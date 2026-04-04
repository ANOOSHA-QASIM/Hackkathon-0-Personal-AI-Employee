"""
Base Watcher - Standalone FileSystem Watcher for Digital FTE Vault.
Monitors /Inbox for new files and creates task files in /Needs_Action.

Usage:
    python base_watcher.py

Prerequisites:
    pip install watchdog pyyaml python-dotenv
"""

import os
import sys
import time
import shutil
import hashlib
import json
from datetime import datetime
from pathlib import Path

# Try to import dependencies
try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install pyyaml")
    sys.exit(1)

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError:
    print("ERROR: watchdog not installed. Run: pip install watchdog")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("WARNING: python-dotenv not installed. Using default paths.")
    pass


# ============================================================================
# Configuration - Absolute Paths per Constitution
# ============================================================================

# Get vault root from environment or use default (absolute path)
VAULT_ROOT = Path(os.environ.get(
    'VAULT_ROOT',
    'E:/hackathon_0_digital_fte/AI_Employee_vault'
))

INBOX_PATH = VAULT_ROOT / 'Inbox'
NEEDS_ACTION_PATH = VAULT_ROOT / 'Needs_Action'
LOGS_PATH = VAULT_ROOT / 'Logs'

# Watcher settings
POLL_INTERVAL = int(os.environ.get('WATCHER_POLL_INTERVAL', '60'))


# ============================================================================
# Audit Logger
# ============================================================================

def get_today_log_path():
    """Get path to today's log file."""
    today = datetime.now().strftime('%Y-%m-%d')
    return LOGS_PATH / f'{today}.json'


def log_action(action_type, file_path, status, metadata=None, error_message=None):
    """Log an action to today's audit file."""
    import json
    
    log_path = get_today_log_path()
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
    
    # Create log entry
    entry = {
        'timestamp': datetime.now().isoformat() + 'Z',
        'action_type': action_type,
        'agent_id': 'filesystem-watcher',
        'file_path': file_path,
        'status': status,
    }
    
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
# Metadata Generation
# ============================================================================

def sanitize_filename(filename):
    """Sanitize filename for safe filesystem use."""
    # Remove .md extension if present
    if filename.lower().endswith('.md'):
        filename = filename[:-3]
    
    # Replace spaces and special chars
    sanitized = filename.replace(' ', '_').replace('/', '_').replace('\\', '_')
    sanitized = ''.join(c for c in sanitized if c.isalnum() or c in '_-')
    
    # Limit length
    if len(sanitized) > 50:
        sanitized = sanitized[:50]
    
    return sanitized


def generate_unique_filename(original_name):
    """Generate unique filename with timestamp prefix."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    sanitized = sanitize_filename(original_name)
    return f"{timestamp}_{sanitized}.md"


def generate_frontmatter(metadata):
    """Generate YAML frontmatter string."""
    return '---\n' + yaml.dump(metadata, sort_keys=False, allow_unicode=True, default_flow_style=False) + '---\n'


def create_task_metadata(original_name, file_type='file_drop', tags=None):
    """Create standard task metadata dictionary."""
    metadata = {
        'status': 'Needs_Action',
        'type': file_type,
        'original_name': original_name,
        'received_timestamp': datetime.now().isoformat() + 'Z',
    }
    
    if tags:
        metadata['tags'] = tags
    
    return metadata


def generate_markdown_content(frontmatter, body=''):
    """Generate complete Markdown file with YAML frontmatter."""
    return generate_frontmatter(frontmatter) + '\n' + body


# ============================================================================
# File Handler
# ============================================================================

class InboxHandler(FileSystemEventHandler):
    """Handler for file creation events in /Inbox."""
    
    def __init__(self):
        super().__init__()
        self.processed_files = set()
    
    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return
        
        file_path = Path(event.src_path)
        
        # Debounce: wait for file to be fully written
        time.sleep(0.5)
        
        # Skip already processed files
        if event.src_path in self.processed_files:
            return
        
        self.processed_files.add(event.src_path)
        process_new_file(file_path)


def process_new_file(file_path):
    """
    Process a new file detected in /Inbox.
    
    Moves file from /Inbox to /Needs_Action and creates paired .md metadata file.
    Uses shutil.move to ensure original file is removed from Inbox.
    """
    print(f"[Watcher] File detected: {file_path.name}")
    
    try:
        # Wait for file to be fully written (Windows file locking)
        time.sleep(0.5)
        
        # Check file size (skip >100MB)
        file_size = file_path.stat().st_size
        if file_size > 100 * 1024 * 1024:
            print(f"[Watcher] Skipping large file: {file_path.name} ({file_size:,} bytes)")
            log_action(
                action_type='error',
                file_path=str(file_path),
                status='blocked',
                error_message=f'File too large: {file_size:,} bytes (>100MB limit)'
            )
            return
        
        # Determine file type
        extension = file_path.suffix.lower()
        file_type_map = {
            '.pdf': 'document',
            '.doc': 'document',
            '.docx': 'document',
            '.txt': 'document',
            '.md': 'document',
            '.xls': 'spreadsheet',
            '.xlsx': 'spreadsheet',
            '.csv': 'spreadsheet',
            '.jpg': 'image',
            '.jpeg': 'image',
            '.png': 'image',
        }
        file_type = file_type_map.get(extension, 'file_drop')
        
        # Generate tags
        tags = [file_type]
        if 'invoice' in file_path.name.lower():
            tags.append('invoice')
        if 'urgent' in file_path.name.lower():
            tags.append('urgent')
        
        # Generate unique filename for .md file
        md_filename = generate_unique_filename(file_path.name)
        md_path = NEEDS_ACTION_PATH / md_filename
        
        # Create metadata with path reference
        metadata = create_task_metadata(file_path.name, file_type, tags)
        metadata['path'] = f'../Needs_Action/{md_filename}'
        
        # Generate content
        content = generate_markdown_content(
            metadata,
            f"""## Task Description

**File**: {file_path.name}
**Type**: {file_type}
**Size**: {file_size:,} bytes
**Detected**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Original Path**: {file_path}
**Moved To**: {NEEDS_ACTION_PATH}

## Action Required

Review and process this file.
"""
        )
        
        # Ensure destination directory exists
        NEEDS_ACTION_PATH.mkdir(parents=True, exist_ok=True)
        
        # Move file from Inbox to Needs_Action (atomic operation)
        dest_file_path = NEEDS_ACTION_PATH / file_path.name
        try:
            shutil.move(str(file_path), str(dest_file_path))
            print(f"[Watcher] Moved: {file_path.name} → Needs_Action/")
            
            # Log move action
            log_action(
                action_type='file_moved',
                file_path=str(dest_file_path),
                status='completed',
                metadata={
                    'source_path': str(file_path),
                    'destination_path': str(dest_file_path),
                    'original_name': file_path.name,
                }
            )
            
        except PermissionError as e:
            print(f"[Watcher] PermissionError moving file: {e}")
            log_action(
                action_type='error',
                file_path=str(file_path),
                status='error',
                error_message=f'Permission denied: {str(e)}'
            )
            # Still create metadata file even if move fails
            return
        
        # Write .md file
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[Watcher] Created task: {md_filename}")
        
        # Log metadata creation
        log_action(
            action_type='metadata_created',
            file_path=str(md_path),
            status='completed',
            metadata={
                'original_name': file_path.name,
                'file_type': file_type,
            }
        )
        
    except Exception as e:
        print(f"[Watcher] Error processing file: {e}")
        log_action(
            action_type='error',
            file_path=str(file_path),
            status='error',
            error_message=str(e)
        )


# ============================================================================
# Main Watcher Loop
# ============================================================================

def ensure_directories():
    """Ensure all required directories exist."""
    for path in [INBOX_PATH, NEEDS_ACTION_PATH, LOGS_PATH]:
        path.mkdir(parents=True, exist_ok=True)


def create_initial_log():
    """Create initial log entry for system initialization."""
    log_action(
        action_type='system_init',
        file_path=str(VAULT_ROOT),
        status='completed',
        metadata={
            'message': 'FileSystem Watcher initialized',
            'phase': 1,
            'phase_name': 'Bronze: Foundation',
            'inbox_path': str(INBOX_PATH),
        }
    )


def run_watcher():
    """Main watcher entry point."""
    print("=" * 60)
    print("Digital FTE - FileSystem Watcher")
    print("=" * 60)
    print()
    
    # Ensure directories exist
    ensure_directories()
    
    # Create initial log entry
    create_initial_log()
    
    print(f"Monitoring Inbox at: {INBOX_PATH}")
    print(f"Poll interval: {POLL_INTERVAL} seconds")
    print("Press Ctrl+C to stop")
    print()
    
    # Set up observer
    event_handler = InboxHandler()
    observer = Observer()
    observer.schedule(event_handler, str(INBOX_PATH), recursive=False)
    
    try:
        observer.start()
        print("[Watcher] Started successfully")
        
        while True:
            time.sleep(POLL_INTERVAL)
            
    except KeyboardInterrupt:
        print("\n[Watcher] Stopped by user")
        observer.stop()
    
    observer.join()
    print("[Watcher] Shutdown complete")


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == '__main__':
    run_watcher()
