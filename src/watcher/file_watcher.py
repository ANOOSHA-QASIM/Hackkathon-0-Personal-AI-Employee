"""
FileSystem Watcher for Digital FTE Vault.
Monitors /Inbox directory for new files and creates task files in /Needs_Action.
"""

import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from .base_watcher import BaseWatcher
from .metadata import sanitize_filename
from ..config.settings import INBOX_PATH, WATCHER_POLL_INTERVAL


class InboxHandler(FileSystemEventHandler):
    """Handler for file creation events in /Inbox."""
    
    def __init__(self, watcher_callback):
        """
        Initialize handler.
        
        Args:
            watcher_callback: Function to call when new file detected
        """
        self.watcher_callback = watcher_callback
        self.processed_files = set()
    
    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return
        
        # Debounce: ignore files created within last 2 seconds (still being written)
        file_path = Path(event.src_path)
        try:
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            if (datetime.now() - mtime).total_seconds() < 2:
                return
        except (OSError, ValueError):
            return
        
        # Skip already processed files
        if event.src_path in self.processed_files:
            return
        
        self.processed_files.add(event.src_path)
        self.watcher_callback(event)


class FileSystemWatcher(BaseWatcher):
    """
    FileSystem Watcher that monitors /Inbox for new files.
    
    When a new file is detected, creates a corresponding .md task file
    in /Needs_Action with YAML frontmatter metadata.
    """
    
    def __init__(self, poll_interval: int = None):
        """
        Initialize FileSystem Watcher.
        
        Args:
            poll_interval: Override default poll interval (seconds)
        """
        super().__init__(
            name='filesystem-watcher',
            poll_interval_seconds=poll_interval or WATCHER_POLL_INTERVAL
        )
        self.observer: Observer = None
        self.event_queue: List[Dict[str, Any]] = []
        self.handler = InboxHandler(self._on_file_detected)
    
    def _on_file_detected(self, event):
        """
        Internal callback when new file detected.
        
        Args:
            event: Watchdog file creation event
        """
        self.event_queue.append({
            'path': event.src_path,
            'name': Path(event.src_path).name,
            'timestamp': datetime.now().isoformat(),
        })
        print(f"[{self.name}] File detected: {Path(event.src_path).name}")
    
    def check(self) -> List[Dict[str, Any]]:
        """
        Check for new events in queue.
        
        Returns:
            List of event dictionaries
        """
        events = self.event_queue.copy()
        self.event_queue.clear()
        return events
    
    def transform_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform file event into task metadata.
        
        Args:
            event: File event dictionary with path, name, timestamp
            
        Returns:
            Task metadata dictionary
        """
        file_path = Path(event['path'])
        file_size = 0
        
        try:
            file_size = file_path.stat().st_size
        except OSError:
            pass
        
        # Check for large files (>100MB)
        if file_size > 100 * 1024 * 1024:
            self.audit_logger.log_action(
                action_type='error',
                file_path=event['path'],
                status='blocked',
                error_message=f'File too large: {file_size} bytes (>100MB limit)',
                metadata={'size_bytes': file_size}
            )
            print(f"[{self.name}] Skipping large file: {event['name']} ({file_size} bytes)")
            return None
        
        # Determine file type from extension
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
            '.gif': 'image',
        }
        
        file_type = file_type_map.get(extension, 'file_drop')
        
        # Generate tags based on file type
        tags = [file_type]
        if 'invoice' in event['name'].lower():
            tags.append('invoice')
        if 'urgent' in event['name'].lower():
            tags.append('urgent')
        
        return {
            'type': 'file_drop',
            'original_name': event['name'],
            'content': f"""## Task Description

**File**: {event['name']}
**Type**: {file_type}
**Size**: {file_size:,} bytes
**Detected**: {event['timestamp']}

## Action Required

Review and process this file.
""",
            'tags': tags,
        }
    
    def start(self):
        """Start the file system observer."""
        # Ensure inbox directory exists
        INBOX_PATH.mkdir(parents=True, exist_ok=True)
        
        # Set up observer
        self.observer = Observer()
        self.observer.schedule(self.handler, str(INBOX_PATH), recursive=False)
        self.observer.start()
        print(f"[{self.name}] Watching {INBOX_PATH} for new files...")
    
    def stop(self):
        """Stop the file system observer."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            print(f"[{self.name}] Watcher stopped")


def run_watcher():
    """Entry point for running the FileSystem Watcher."""
    watcher = FileSystemWatcher()
    watcher.start()
    
    try:
        watcher.run()
    except KeyboardInterrupt:
        watcher.stop()


if __name__ == '__main__':
    run_watcher()
