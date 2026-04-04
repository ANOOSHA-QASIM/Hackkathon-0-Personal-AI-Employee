"""
LinkedIn Post Scheduler - Checks scheduled posts and publishes at the right time.

Usage:
    python src/linkedin/post_scheduler.py
"""

import os
import sys
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
import yaml

# Paths
VAULT_ROOT = Path(os.environ.get(
    'VAULT_ROOT',
    'E:/hackathon_0_digital_fte/AI_Employee_vault'
))
APPROVED_PATH = VAULT_ROOT / 'Approved'
DONE_PATH = VAULT_ROOT / 'Done'
LOGS_PATH = VAULT_ROOT / 'Logs'


def parse_post_metadata(file_path):
    """Parse YAML frontmatter from post file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not content.startswith('---'):
        return None
    
    end = content.find('---', 3)
    if end == -1:
        return None
    
    yaml_content = content[3:end].strip()
    try:
        return yaml.safe_load(yaml_content)
    except yaml.YAMLError:
        return None


def log_action(action_type, file_path, status, metadata=None, error_message=None):
    """Log an action to today's audit file."""
    today = datetime.now().strftime('%Y-%m-%d')
    log_path = LOGS_PATH / f'{today}.json'
    
    LOGS_PATH.mkdir(parents=True, exist_ok=True)
    
    # Load or initialize log file
    if log_path.exists():
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            log_data = {'date': today, 'vault_id': 'AI_Employee_vault', 'entries': [], 'summary': {}}
    else:
        log_data = {'date': today, 'vault_id': 'AI_Employee_vault', 'entries': [], 'summary': {}}
    
    # Create log entry
    entry = {
        'timestamp': datetime.now().isoformat() + 'Z',
        'action_type': action_type,
        'agent_id': 'linkedin-scheduler',
        'file_path': file_path,
        'status': status,
        'source': 'linkedin',
    }
    
    if metadata:
        entry['metadata'] = metadata
    if error_message:
        entry['error_message'] = error_message
    
    # Append entry
    log_data['entries'].append(entry)
    log_data['summary']['total_actions'] = len(log_data['entries'])
    
    # Write back
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2)


def check_scheduled_posts():
    """Check /Approved for posts scheduled for current time."""
    print("[Scheduler] Checking for scheduled posts...")
    
    if not APPROVED_PATH.exists():
        print("[Scheduler] /Approved folder not found")
        return
    
    now = datetime.now()
    
    # Find LinkedIn posts in /Approved
    for post_file in APPROVED_PATH.glob('*.md'):
        try:
            # Parse metadata
            metadata = parse_post_metadata(post_file)
            
            if not metadata:
                continue
            
            # Check if it's a LinkedIn post
            if metadata.get('platform') != 'linkedin':
                continue
            
            # Check if scheduled
            scheduled_time_str = metadata.get('scheduled_time')
            if not scheduled_time_str:
                continue  # Not scheduled, will be handled by poster
            
            # Parse scheduled time
            try:
                scheduled_time = datetime.fromisoformat(scheduled_time_str.replace('Z', '+00:00'))
            except:
                print(f"[Scheduler] Invalid scheduled time in {post_file.name}")
                continue
            
            # Check if it's time to publish (within 2-minute window)
            time_diff = abs((now - scheduled_time).total_seconds())
            if time_diff <= 120:  # 2 minutes
                print(f"[Scheduler] Time to publish: {post_file.name}")
                
                # Update status to indicate ready for publishing
                # The linkedin_poster.py will handle actual publishing
                log_action(
                    action_type='scheduled_post_ready',
                    file_path=str(post_file),
                    status='completed',
                    metadata={
                        'scheduled_time': scheduled_time_str,
                        'time_diff_seconds': time_diff
                    },
                    source='linkedin'
                )
            
        except Exception as e:
            print(f"[Scheduler] Error processing {post_file.name}: {e}")
            log_action(
                action_type='scheduler_error',
                file_path=str(post_file),
                status='error',
                error_message=str(e),
                source='linkedin'
            )


def run_scheduler():
    """Run scheduler continuously (check every 30 seconds)."""
    print("=" * 60)
    print("Digital FTE - LinkedIn Post Scheduler")
    print("=" * 60)
    print()
    print(f"Monitoring /Approved for scheduled posts every 30 seconds...")
    print("Press Ctrl+C to stop")
    print()
    
    while True:
        try:
            check_scheduled_posts()
            time.sleep(30)  # 30 seconds
        except KeyboardInterrupt:
            print("\n[Scheduler] Stopped by user")
            break
        except Exception as e:
            print(f"[Scheduler] Error in scheduler loop: {e}")
            time.sleep(60)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # Run once (for testing)
        check_scheduled_posts()
    else:
        # Run continuously
        run_scheduler()
