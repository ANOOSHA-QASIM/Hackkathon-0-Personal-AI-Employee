"""
Gmail Monitor - Fetches unread emails and creates alerts in /Needs_Action.

Usage:
    python src/gmail/gmail_monitor.py

Prerequisites:
    pip install google-auth-oauthlib google-api-python-client
    credentials.json in vault root (Gmail API OAuth2 credentials)
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path
from email import message_from_string
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import yaml

# ============================================================================
# Configuration - Absolute Paths per Constitution
# ============================================================================

VAULT_ROOT = Path(os.environ.get(
    'VAULT_ROOT',
    'E:/hackathon_0_digital_fte/AI_Employee_vault'
))

INBOX_PATH = VAULT_ROOT / 'Inbox'
NEEDS_ACTION_PATH = VAULT_ROOT / 'Needs_Action'
LOGS_PATH = VAULT_ROOT / 'Logs'
CREDENTIALS_PATH = VAULT_ROOT / 'credentials.json'
PROCESSED_EMAILS_PATH = LOGS_PATH / 'processed_emails.json'

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Triage keywords for priority classification
TRIAGE_KEYWORDS = {
    'high': ['urgent', 'asap', 'invoice', 'payment', 'emergency', 'action required', 'overdue'],
    'low': ['newsletter', 'notification', 'update', 'digest', 'unsubscribe']
}

# VIP senders (customize as needed)
VIP_SENDERS = []


# ============================================================================
# Audit Logging
# ============================================================================

def log_action(action_type, file_path, status, metadata=None, error_message=None, **kwargs):
    """Log an action to today's audit file.
    
    Args:
        action_type: Type of action (email_checked, email_alert_created, etc.)
        file_path: Path to affected file
        status: Action status (completed, error, etc.)
        metadata: Optional additional metadata
        error_message: Optional error message
        **kwargs: Additional fields to include in log entry (e.g., source='gmail')
    """
    today = datetime.now().strftime('%Y-%m-%d')
    log_path = LOGS_PATH / f'{today}.json'

    LOGS_PATH.mkdir(parents=True, exist_ok=True)

    # Load or initialize log file
    if log_path.exists():
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            log_data = _initialize_log_data()
    else:
        log_data = _initialize_log_data()

    # Create log entry with kwargs support
    entry = {
        'timestamp': datetime.now().isoformat() + 'Z',
        'action_type': action_type,
        'agent_id': 'gmail-monitor',
        'file_path': file_path,
        'status': status,
    }
    
    # Add any additional kwargs (e.g., source='gmail')
    for key, value in kwargs.items():
        entry[key] = value

    if metadata:
        entry['metadata'] = metadata
    if error_message:
        entry['error_message'] = error_message

    # Append entry
    log_data['entries'].append(entry)

    # Update summary
    log_data['summary'] = {
        'total_actions': len(log_data['entries']),
        'completed': sum(1 for e in log_data['entries'] if e['status'] == 'completed'),
        'errors': sum(1 for e in log_data['entries'] if e['status'] == 'error'),
    }

    # Write back
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2)


def _initialize_log_data():
    """Initialize new log file structure."""
    today = datetime.now().strftime('%Y-%m-%d')
    return {
        'date': today,
        'vault_id': 'AI_Employee_vault',
        'entries': [],
        'summary': {
            'total_actions': 0,
            'completed': 0,
            'errors': 0,
        },
        'sealed': False,
        'sealed_at': None,
        'content_hash': None,
    }


# ============================================================================
# Gmail Authentication
# ============================================================================

def get_gmail_credentials():
    """Get Gmail API credentials."""
    creds = None
    
    if CREDENTIALS_PATH.exists():
        creds = Credentials.from_authorized_user_file(CREDENTIALS_PATH, SCOPES)
    
    # If credentials don't exist or are invalid, prompt for auth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            # Save refreshed credentials
            with open(CREDENTIALS_PATH, 'w') as f:
                f.write(creds.to_json())
        else:
            print("Please authenticate Gmail API...")
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
            
            # Save credentials for future use
            with open(CREDENTIALS_PATH, 'w') as f:
                f.write(creds.to_json())
    
    return creds


# ============================================================================
# Email Processing
# ============================================================================

def load_processed_emails():
    """Load set of processed email message IDs."""
    if not PROCESSED_EMAILS_PATH.exists():
        # Create file with empty list if it doesn't exist
        PROCESSED_EMAILS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(PROCESSED_EMAILS_PATH, 'w', encoding='utf-8') as f:
            json.dump({'message_ids': [], 'last_updated': datetime.now().isoformat() + 'Z'}, f, indent=2)
        return set()
    
    try:
        with open(PROCESSED_EMAILS_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
            if not content.strip():
                # File is empty, initialize with empty list
                data = {'message_ids': []}
            else:
                data = json.loads(content)
            return set(data.get('message_ids', []))
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"[Gmail] Warning: Could not load processed emails: {e}")
        # Return empty set and recreate file
        PROCESSED_EMAILS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(PROCESSED_EMAILS_PATH, 'w', encoding='utf-8') as f:
            json.dump({'message_ids': [], 'last_updated': datetime.now().isoformat() + 'Z'}, f, indent=2)
        return set()


def save_processed_email(message_id):
    """Mark an email as processed."""
    processed = load_processed_emails()
    processed.add(message_id)
    
    PROCESSED_EMAILS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROCESSED_EMAILS_PATH, 'w', encoding='utf-8') as f:
        json.dump({
            'message_ids': list(processed),
            'last_updated': datetime.now().isoformat() + 'Z'
        }, f, indent=2)


def is_email_processed(message_id):
    """Check if email was already processed."""
    processed = load_processed_emails()
    return message_id in processed


def classify_priority(sender: str, subject: str) -> str:
    """Classify email priority based on keywords and sender."""
    subject_lower = subject.lower()
    
    # VIP sender → High priority
    if sender in VIP_SENDERS:
        return 'high'
    
    # High-priority keywords
    for keyword in TRIAGE_KEYWORDS['high']:
        if keyword in subject_lower:
            return 'high'
    
    # Low-priority keywords
    for keyword in TRIAGE_KEYWORDS['low']:
        if keyword in subject_lower:
            return 'low'
    
    return 'normal'


def decode_email_payload(payload):
    """Decode email body from Gmail API payload."""
    if 'body' in payload and 'data' in payload['body']:
        return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8')
    
    # Multipart email - try to get plain text part
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain':
                if 'body' in part and 'data' in part['body']:
                    return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
    
    return ''


def create_email_alert(service, message_id):
    """
    Fetch email from Gmail and create alert in /Needs_Action.
    
    Args:
        service: Gmail API service
        message_id: Gmail message ID
    """
    try:
        # Fetch email
        message = service.users().messages().get(
            userId='me',
            id=message_id,
            format='full'
        ).execute()
        
        # Extract headers
        headers = message['payload']['headers']
        subject = ''
        sender = ''
        sender_name = ''
        date = ''
        
        for header in headers:
            if header['name'] == 'Subject':
                subject = header['value']
            elif header['name'] == 'From':
                sender_full = header['value']
                # Parse "Name <email@example.com>" format
                if '<' in sender_full and '>' in sender_full:
                    sender_name = sender_full.split('<')[0].strip()
                    sender = sender_full.split('<')[1].split('>')[0]
                else:
                    sender = sender_full
            elif header['name'] == 'Date':
                date = header['value']
        
        # Check if already processed
        if is_email_processed(message_id):
            print(f"[Gmail] Skipping already processed: {subject}")
            log_action(
                action_type='email_skipped',
                file_path=f'Gmail:{message_id}',
                status='completed',
                metadata={
                    'subject': subject,
                    'message_id': message_id,
                    'reason': 'already_processed'
                },
                source='gmail'
            )
            return
        
        # Decode body
        body = decode_email_payload(message['payload'])
        
        # Classify priority
        priority = classify_priority(sender, subject)
        
        # Generate tags
        tags = ['email']
        if priority == 'high':
            tags.append('urgent')
        if 'invoice' in subject.lower():
            tags.append('invoice')
        if 'payment' in subject.lower():
            tags.append('payment')
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        sanitized_subject = subject.replace(' ', '_').replace('/', '_')[:30]
        filename = f"{timestamp}_email_{sanitized_subject}.md"
        
        # Create metadata
        metadata = {
            'status': 'Needs_Action',
            'type': 'email_alert',
            'sender': sender,
            'sender_name': sender_name,
            'subject': subject,
            'received_timestamp': datetime.now().isoformat() + 'Z',
            'message_id': message_id,
            'priority': priority,
            'tags': tags,
            'processed': False,
        }
        
        # Generate content
        yaml_content = yaml.dump(metadata, sort_keys=False, allow_unicode=True, default_flow_style=False)
        content = f"---\n{yaml_content}---\n\n"
        content += f"## Email Content\n\n"
        content += f"**From**: {sender_name} <{sender}>\n"
        content += f"**Date**: {date}\n\n"
        content += f"{body}\n"
        
        # Write alert file
        NEEDS_ACTION_PATH.mkdir(parents=True, exist_ok=True)
        alert_path = NEEDS_ACTION_PATH / filename
        
        with open(alert_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Mark as processed
        save_processed_email(message_id)
        
        print(f"[Gmail] Created alert: {filename} (priority: {priority})")
        
        # Log action
        log_action(
            action_type='email_alert_created',
            file_path=str(alert_path),
            status='completed',
            metadata={
                'subject': subject,
                'sender': sender,
                'priority': priority,
                'message_id': message_id,
            },
            source='gmail'
        )
        
    except Exception as e:
        print(f"[Gmail] Error processing email {message_id}: {e}")
        log_action(
            action_type='email_processing_error',
            file_path=f'Gmail:{message_id}',
            status='error',
            error_message=str(e),
            source='gmail'
        )


# ============================================================================
# Main Gmail Monitor
# ============================================================================

def check_unread_emails():
    """Check Gmail for unread emails and create alerts."""
    print("[Gmail] Checking for unread emails...")
    
    try:
        creds = get_gmail_credentials()
        service = build('gmail', 'v1', credentials=creds)
        
        # Query unread emails (max 5 at a time)
        results = service.users().messages().list(
            userId='me',
            q='is:unread',
            maxResults=5
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            print("[Gmail] No unread emails found")
            log_action(
                action_type='gmail_check',
                file_path=str(GMAIL_PATH),
                status='completed',
                metadata={'unread_count': 0},
                source='gmail'
            )
            return
        
        print(f"[Gmail] Found {len(messages)} unread emails")
        
        # Process each email
        for message in messages:
            create_email_alert(service, message['id'])
        
        log_action(
            action_type='gmail_check_complete',
            file_path=str(NEEDS_ACTION_PATH),
            status='completed',
            metadata={
                'unread_count': len(messages),
                'alerts_created': len(messages)
            },
            source='gmail'
        )
        
    except FileNotFoundError:
        print("[Gmail] ERROR: credentials.json not found. Please authenticate Gmail first.")
        print("Run: python src/gmail/gmail_auth.py --authenticate")
        log_action(
            action_type='gmail_error',
            file_path=str(CREDENTIALS_PATH),
            status='error',
            error_message='credentials.json not found',
            source='gmail'
        )
    except Exception as e:
        print(f"[Gmail] Error checking emails: {e}")
        log_action(
            action_type='gmail_check_error',
            file_path=str(VAULT_ROOT),
            status='error',
            error_message=str(e),
            source='gmail'
        )


def run_monitor():
    """Run Gmail monitor continuously (check every 5 minutes)."""
    import time
    
    print("=" * 60)
    print("Digital FTE - Gmail Monitor")
    print("=" * 60)
    print()
    print(f"Monitoring Gmail every 5 minutes...")
    print("Press Ctrl+C to stop")
    print()
    
    while True:
        try:
            check_unread_emails()
            time.sleep(300)  # 5 minutes
        except KeyboardInterrupt:
            print("\n[Gmail] Stopped by user")
            break
        except Exception as e:
            print(f"[Gmail] Error in monitor loop: {e}")
            time.sleep(60)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # Run once (for testing)
        check_unread_emails()
    else:
        # Run continuously
        run_monitor()
