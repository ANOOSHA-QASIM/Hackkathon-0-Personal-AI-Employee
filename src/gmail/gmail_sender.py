"""
Gmail Sender - Watches /Approved/Gmail and sends drafted replies.

Usage:
    python src/gmail/gmail_sender.py

Features:
- Watches /Approved/Gmail for approved draft replies
- Sends emails using Gmail API
- Moves sent emails to /Done
"""

import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import base64
import yaml

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import VAULT_ROOT, LOGS_PATH, DONE_PATH
from gmail.gmail_monitor import get_gmail_credentials
from gmail.gmail_auth import authenticate_gmail

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Paths
APPROVED_PATH = VAULT_ROOT / 'Approved'
APPROVED_GMAIL_PATH = APPROVED_PATH / 'Gmail'


def log_action(action_type, file_path, status, metadata=None, error_message=None, **kwargs):
    """Log an action to today's audit file.
    
    Args:
        action_type: Type of action
        file_path: Path to affected file
        status: Action status
        metadata: Optional additional metadata
        error_message: Optional error message
        **kwargs: Additional fields (e.g., source='gmail')
    """
    today = datetime.now().strftime('%Y-%m-%d')
    log_path = LOGS_PATH / f'{today}.json'

    LOGS_PATH.mkdir(parents=True, exist_ok=True)

    # Load or initialize
    if log_path.exists():
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            log_data = {'date': today, 'vault_id': 'AI_Employee_vault', 'entries': [], 'summary': {}}
    else:
        log_data = {'date': today, 'vault_id': 'AI_Employee_vault', 'entries': [], 'summary': {}}

    entry = {
        'timestamp': datetime.now().isoformat() + 'Z',
        'action_type': action_type,
        'agent_id': 'gmail-sender',
        'file_path': file_path,
        'status': status,
    }
    
    # Add kwargs (e.g., source='gmail')
    for key, value in kwargs.items():
        entry[key] = value

    if metadata:
        entry['metadata'] = metadata
    if error_message:
        entry['error_message'] = error_message

    log_data['entries'].append(entry)
    log_data['summary']['total_actions'] = len(log_data['entries'])

    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2)


def parse_frontmatter(file_path):
    """Parse YAML frontmatter from Markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not content.startswith('---'):
        return None, content
    
    end = content.find('---', 3)
    if end == -1:
        return None, content
    
    yaml_content = content[3:end].strip()
    try:
        metadata = yaml.safe_load(yaml_content)
        body = content[end + 3:].strip()
        return metadata, body
    except yaml.YAMLError:
        return None, content


def extract_draft_reply(content):
    """Extract draft reply from Markdown content."""
    # Look for "## Draft Reply" section
    if '## Draft Reply' in content:
        parts = content.split('## Draft Reply')
        if len(parts) > 1:
            # Get content after "## Draft Reply"
            draft_section = parts[1].strip()
            # Remove any subsequent sections
            if '---' in draft_section:
                draft_section = draft_section.split('---')[0].strip()
            # Remove "## Actions" if present
            if '## Actions' in draft_section:
                draft_section = draft_section.split('## Actions')[0].strip()
            return draft_section
    
    # Fallback: return everything after last "---"
    if content.count('---') >= 2:
        parts = content.split('---')
        return parts[-1].strip()
    
    return content


def send_email(service, to_email, subject, body, in_reply_to=None):
    """
    Send email using Gmail API.

    Args:
        service: Gmail API service
        to_email: Recipient email address
        subject: Email subject
        body: Email body text
        in_reply_to: Optional message ID to reply to

    Returns:
        Sent message ID
    """
    # Create message
    message = MIMEMultipart()
    message['to'] = to_email
    message['subject'] = subject

    # Add In-Reply-To header for threading
    if in_reply_to:
        message['In-Reply-To'] = in_reply_to
        message['References'] = in_reply_to

    # Add body
    message.attach(MIMEText(body, 'plain'))

    # Encode message
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

    try:
        # Send email
        sent_message = service.users().messages().send(
            userId='me',
            body={'raw': raw_message}
        ).execute()

        message_id = sent_message['id']
        
        # Print clear success message
        print()
        print("=" * 60)
        print("SUCCESS: Email Sent!")
        print("=" * 60)
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Message ID: {message_id}")
        print("=" * 60)
        print()

        return message_id
    except HttpError as error:
        print(f"[Gmail Sender] API error: {error}")
        raise


def check_approved_gmail():
    """Check /Approved/Gmail for drafts to send.
    
    SMART FOLDER LOGIC: Files in /Approved/Gmail are assumed approved by default.
    Bypasses metadata checks for status and hitl_approved.
    """
    print("[Gmail Sender] Checking /Approved/Gmail for drafts...")

    if not APPROVED_GMAIL_PATH.exists():
        # Create it if it doesn't exist
        APPROVED_GMAIL_PATH.mkdir(parents=True, exist_ok=True)
        print("[Gmail Sender] Created /Approved/Gmail folder")
        return

    # Find ALL .md files in /Approved/Gmail (smart folder logic)
    print(f"[Gmail Sender] Scanning for .md files in {APPROVED_GMAIL_PATH}")
    md_files = list(APPROVED_GMAIL_PATH.glob('*.md'))
    print(f"[Gmail Sender] Found {len(md_files)} .md file(s)")
    
    for draft_file in md_files:
        try:
            print(f"[Gmail Sender] Processing: {draft_file.name}")

            # Parse metadata
            metadata, content = parse_frontmatter(draft_file)

            # SMART FOLDER: If no metadata, create minimal metadata
            if not metadata:
                print(f"[Gmail Sender] WARNING: {draft_file.name} has no metadata - assuming approved")
                metadata = {
                    'status': 'approved',
                    'hitl_approved': True,
                    'draft_type': 'reply',
                }
            
            # SMART FOLDER: Assume approved if in /Approved/Gmail
            # Skip only if explicitly marked as sent
            if metadata.get('status') == 'sent':
                print(f"[Gmail Sender] Already sent: {draft_file.name}")
                continue
            
            # Check if it's a draft reply (or assume it is if in Approved/Gmail)
            if metadata.get('draft_type') != 'reply':
                print(f"[Gmail Sender] WARNING: {draft_file.name} draft_type missing - assuming reply")
            
            # Get recipient (original sender) - REQUIRED
            recipient = metadata.get('sender')
            if not recipient:
                print(f"[Gmail Sender] ERROR: {draft_file.name} - Missing 'sender' metadata")
                print(f"[Gmail Sender]   Action: Add 'sender: email@example.com' to the file metadata")
                log_action(
                    action_type='gmail_send_skipped',
                    file_path=str(draft_file),
                    status='skipped',
                    error_message='Missing sender metadata',
                    source='gmail'
                )
                continue

            # Get subject (add Re: prefix if not present)
            subject = metadata.get('subject', 'No Subject')
            if not subject.startswith('Re:'):
                subject = f"Re: {subject}"

            # Get original message ID for threading
            message_id = metadata.get('message_id', None)

            # Extract draft reply
            draft_reply = extract_draft_reply(content)

            if not draft_reply:
                print(f"[Gmail Sender] ERROR: {draft_file.name} - No draft reply content found")
                print(f"[Gmail Sender]   Action: Add draft reply content after '## Draft Reply' section")
                log_action(
                    action_type='gmail_send_skipped',
                    file_path=str(draft_file),
                    status='skipped',
                    error_message='No draft reply content',
                    source='gmail'
                )
                continue

            # Get Gmail credentials
            print("[Gmail Sender] Authenticating with Gmail...")
            creds = get_gmail_credentials()

            if not creds or not creds.valid:
                print("[Gmail Sender] Gmail authentication failed")
                log_action(
                    action_type='gmail_auth_failed',
                    file_path=str(draft_file),
                    status='error',
                    error_message='Gmail authentication failed',
                    source='gmail'
                )
                continue

            # Build Gmail service
            service = build('gmail', 'v1', credentials=creds)

            # Send email
            print(f"[Gmail Sender] Sending email to {recipient}...")
            sent_message_id = send_email(service, recipient, subject, draft_reply, message_id)
            
            print(f"[Gmail Sender] Email sent! Message ID: {sent_message_id}")
            
            # Update draft file
            metadata['status'] = 'sent'
            metadata['sent_at'] = datetime.now().isoformat() + 'Z'
            metadata['sent_message_id'] = sent_message_id
            
            # Write updated metadata
            yaml_content = yaml.dump(metadata, sort_keys=False, allow_unicode=True, default_flow_style=False)
            updated_content = f"---\n{yaml_content}---\n\n{content}"
            
            with open(draft_file, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            
            # Move to /Done
            done_path = DONE_PATH / draft_file.name
            draft_file.rename(done_path)
            print(f"[Gmail Sender] Moved to /Done: {draft_file.name}")
            
            # Log action
            log_action(
                action_type='gmail_sent',
                file_path=str(done_path),
                status='completed',
                metadata={
                    'recipient': recipient,
                    'subject': subject,
                    'sent_message_id': sent_message_id,
                }
            )
            
        except Exception as e:
            print(f"[Gmail Sender] Error processing {draft_file.name}: {e}")
            log_action(
                action_type='gmail_send_error',
                file_path=str(draft_file),
                status='error',
                error_message=str(e)
            )


def run_sender():
    """Run Gmail sender continuously."""
    print("=" * 60)
    print("Digital FTE - Gmail Sender")
    print("=" * 60)
    print()
    print(f"Monitoring /Approved/Gmail every 60 seconds...")
    print("Press Ctrl+C to stop")
    print()
    
    while True:
        try:
            check_approved_gmail()
            time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n[Gmail Sender] Stopped by user")
            break
        except Exception as e:
            print(f"[Gmail Sender] Error in loop: {e}")
            time.sleep(60)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        check_approved_gmail()
    else:
        run_sender()
