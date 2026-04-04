"""
Auto Drafter - Watches /Needs_Action and generates draft replies using LLM.

Usage:
    python src/agent/auto_drafter.py

Features:
- Watches /Needs_Action for new .md files (email tasks)
- Generates draft replies using Groq API (Llama 3.3 70B)
- Saves drafts to /In_Progress with status: drafted
"""

import os
import sys
import time
import json
from datetime import datetime
from pathlib import Path
import yaml

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.settings import VAULT_ROOT, NEEDS_ACTION_PATH, IN_PROGRESS_PATH, LOGS_PATH

# Configuration
POLL_INTERVAL = 30  # Check every 30 seconds
DRAFTS_PATH = IN_PROGRESS_PATH / 'auto-drafter'

# Groq API Configuration
USE_GROQ = os.environ.get('USE_GROQ', 'true').lower() == 'true'
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
GROQ_MODEL = os.environ.get('GROQ_MODEL', 'llama-3.3-70b-versatile')
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'


def log_action(action_type, file_path, status, metadata=None, error_message=None):
    """Log an action to today's audit file."""
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
        'agent_id': 'auto-drafter',
        'file_path': file_path,
        'status': status,
    }
    
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


def generate_draft_llm(email_content, subject, sender):
    """
    Generate draft reply using LLM.

    Args:
        email_content: Original email body
        subject: Email subject
        sender: Sender email address

    Returns:
        Generated draft reply text
    """
    prompt = f"""You are a professional email assistant. Draft a polite, concise reply to the following email.

Original Email:
From: {sender}
Subject: {subject}

Content:
{email_content}

Draft a professional reply. Keep it under 150 words. Be helpful and action-oriented.

Draft Reply:"""

    if USE_GROQ and GROQ_API_KEY:
        return generate_draft_groq(prompt)
    else:
        # Fallback: Use template
        return generate_draft_template(subject, sender)


def generate_draft_groq(prompt):
    """Generate draft using Groq API (Llama 3.3 70B)."""
    try:
        import requests
        
        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'model': GROQ_MODEL,
            'messages': [
                {'role': 'system', 'content': 'You are a professional email assistant. Draft polite, concise replies.'},
                {'role': 'user', 'content': prompt}
            ],
            'max_tokens': 200,
            'temperature': 0.7
        }
        
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        # Extract response
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content'].strip()
        else:
            print(f"[Auto-Drafter] Groq error: No choices in response")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"[Auto-Drafter] Groq API error: {e}")
        return None
    except Exception as e:
        print(f"[Auto-Drafter] Groq error: {e}")
        return None


def generate_draft_template(subject, sender):
    """Generate draft using template (fallback)."""
    return f"""Dear {sender.split('@')[0]},

Thank you for your email regarding "{subject}".

I have received your message and will review it shortly. I will get back to you with a detailed response within 24 hours.

Best regards,
Digital FTE Assistant
"""


def create_draft_reply(source_file, draft_content):
    """
    Create draft reply file in /In_Progress.
    
    Args:
        source_file: Path to original .md file in /Needs_Action
        draft_content: Generated draft reply text
    """
    # Parse original metadata
    metadata, body = parse_frontmatter(source_file)
    
    if not metadata:
        print(f"[Auto-Drafter] Skipping invalid file: {source_file.name}")
        return None
    
    # Check if it's an email alert
    if metadata.get('type') not in ['email_alert', 'email']:
        return None  # Not an email, skip
    
    # Generate draft filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    draft_filename = f"draft_{timestamp}_{source_file.stem}.md"
    
    # Ensure drafts directory exists
    DRAFTS_PATH.mkdir(parents=True, exist_ok=True)
    draft_path = DRAFTS_PATH / draft_filename
    
    # Update metadata for draft
    draft_metadata = metadata.copy()
    draft_metadata['status'] = 'drafted'
    draft_metadata['draft_type'] = 'reply'
    draft_metadata['drafted_at'] = datetime.now().isoformat() + 'Z'
    draft_metadata['drafted_by'] = 'auto-drafter'
    draft_metadata['original_file'] = str(source_file)
    
    # Generate draft content
    yaml_content = yaml.dump(draft_metadata, sort_keys=False, allow_unicode=True, default_flow_style=False)
    
    full_content = f"---\n{yaml_content}---\n\n"
    full_content += "## Original Email\n\n"
    full_content += body
    full_content += "\n\n---\n\n"
    full_content += "## Draft Reply\n\n"
    full_content += draft_content
    full_content += "\n\n---\n\n"
    full_content += "## Actions\n\n"
    full_content += "- [ ] Review and edit draft\n"
    full_content += "- [ ] Send reply (move to /Approved/Gmail)\n"
    
    # Write draft file
    with open(draft_path, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"[Auto-Drafter] Created draft: {draft_filename}")
    
    # Log action
    log_action(
        action_type='draft_created',
        file_path=str(draft_path),
        status='completed',
        metadata={
            'original_file': str(source_file),
            'subject': metadata.get('subject', ''),
            'sender': metadata.get('sender', ''),
        }
    )
    
    return draft_path


def check_needs_action():
    """Check /Needs_Action for new files to draft replies for."""
    print("[Auto-Drafter] Checking /Needs_Action for new files...")
    
    if not NEEDS_ACTION_PATH.exists():
        print("[Auto-Drafter] /Needs_Action folder not found")
        return
    
    # Find .md files
    for md_file in NEEDS_ACTION_PATH.glob('*.md'):
        try:
            # Parse metadata
            metadata, _ = parse_frontmatter(md_file)
            
            if not metadata:
                continue
            
            # Check if already drafted
            if metadata.get('status') == 'drafted':
                continue
            
            # Check if it's an email
            if metadata.get('type') not in ['email_alert', 'email']:
                continue
            
            print(f"[Auto-Drafter] Processing: {md_file.name}")
            
            # Extract email info
            subject = metadata.get('subject', 'No Subject')
            sender = metadata.get('sender', 'Unknown')
            body = metadata.get('body', '')
            
            # Generate draft
            print(f"[Auto-Drafter] Generating draft reply...")
            draft_content = generate_draft_llm(body, subject, sender)
            
            if draft_content:
                # Create draft file
                create_draft_reply(md_file, draft_content)
            
        except Exception as e:
            print(f"[Auto-Drafter] Error processing {md_file.name}: {e}")
            log_action(
                action_type='draft_error',
                file_path=str(md_file),
                status='error',
                error_message=str(e)
            )


def run_drafter():
    """Run auto-drafter continuously."""
    print("=" * 60)
    print("Digital FTE - Auto Drafter")
    print("=" * 60)
    print()
    print(f"Monitoring /Needs_Action every {POLL_INTERVAL} seconds...")
    print("Press Ctrl+C to stop")
    print()
    
    while True:
        try:
            check_needs_action()
            time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print("\n[Auto-Drafter] Stopped by user")
            break
        except Exception as e:
            print(f"[Auto-Drafter] Error in loop: {e}")
            time.sleep(60)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        check_needs_action()
    else:
        run_drafter()
