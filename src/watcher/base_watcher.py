"""
BaseWatcher - Abstract base class for all Digital FTE watchers.

All watchers (FileSystem, Gmail, WhatsApp, LinkedIn) MUST inherit from this class
to ensure consistent logging, metadata generation, and error handling.
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional
from pathlib import Path
import shutil

from .metadata import (
    generate_markdown_content,
    create_task_metadata,
    generate_unique_filename,
)
from ..audit.logger import AuditLogger
from ..config.settings import VAULT_ROOT


class BaseWatcher(ABC):
    """
    Abstract base class for all Sentinel watchers.
    
    Subclasses MUST implement:
    - check(): Detect new events/items from source
    - transform_event(): Convert event to task metadata
    """
    
    def __init__(self, name: str, poll_interval_seconds: int = 60):
        """
        Initialize watcher.
        
        Args:
            name: Unique watcher identifier (e.g., 'filesystem-watcher')
            poll_interval_seconds: How often to check for new events
        """
        self.name = name
        self.poll_interval = poll_interval_seconds
        self.last_check: Optional[datetime] = None
        self.audit_logger = AuditLogger(name)
    
    @abstractmethod
    def check(self) -> List[Dict[str, Any]]:
        """
        Detect new events/items from source.
        
        Returns:
            List of event dictionaries to be processed
        """
        pass
    
    @abstractmethod
    def transform_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform raw event into task metadata format.
        
        Args:
            event: Raw event data from check()
            
        Returns:
            Dictionary with task metadata including:
            - status: 'Needs_Action'
            - type: Source type (e.g., 'file_drop', 'email')
            - original_name: Original identifier
            - received_timestamp: ISO 8601 timestamp
            - tags: List of relevant tags
            - content: Task description/body
        """
        pass
    
    def run(self) -> None:
        """
        Main watcher loop.
        
        Continuously checks for events, transforms them, and creates vault tasks.
        """
        import time
        
        print(f"[{self.name}] Starting watcher (poll interval: {self.poll_interval}s)")
        
        while True:
            try:
                events = self.check()
                print(f"[{self.name}] Detected {len(events)} events")
                
                for event in events:
                    try:
                        task = self.transform_event(event)
                        self.create_vault_task(task)
                    except Exception as e:
                        self.audit_logger.log_action(
                            action_type='error',
                            file_path=event.get('path', 'unknown'),
                            status='error',
                            error_message=str(e)
                        )
                
                self.last_check = datetime.now()
                time.sleep(self.poll_interval)
                
            except KeyboardInterrupt:
                print(f"[{self.name}] Watcher stopped by user")
                break
            except Exception as e:
                print(f"[{self.name}] Error in main loop: {e}")
                time.sleep(self.poll_interval)
    
    def create_vault_task(self, task_metadata: Dict[str, Any]) -> str:
        """
        Create a task file in /Needs_Action with YAML frontmatter.
        
        Args:
            task_metadata: Metadata from transform_event()
            
        Returns:
            Path to created task file
        """
        # Generate unique filename
        original_name = task_metadata.get('original_name', 'untitled')
        filename = generate_unique_filename(original_name)
        
        # Build full path
        needs_action_path = VAULT_ROOT / 'Needs_Action'
        needs_action_path.mkdir(parents=True, exist_ok=True)
        dest_path = needs_action_path / filename
        
        # Generate frontmatter with required fields
        frontmatter = {
            'status': 'Needs_Action',
            'type': task_metadata.get('type', self.name),
            'original_name': original_name,
            'received_timestamp': datetime.now().isoformat() + 'Z',
            'tags': task_metadata.get('tags', []),
        }
        
        # Add optional fields
        if 'priority' in task_metadata:
            frontmatter['priority'] = task_metadata['priority']
        
        # Build content
        content = generate_markdown_content(
            frontmatter,
            task_metadata.get('content', '## Task Description\n\nProcess this item.')
        )
        
        # Write file
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Log action
        self.audit_logger.log_action(
            action_type='metadata_created',
            file_path=str(dest_path),
            status='completed',
            metadata={'original_name': original_name}
        )
        
        print(f"[{self.name}] Created task: {filename}")
        return str(dest_path)
    
    def move_file(self, src_path: str, dest_path: str) -> str:
        """
        Move file from source to destination (claim-by-move protocol).
        
        Args:
            src_path: Source file path
            dest_path: Destination file path
            
        Returns:
            Destination path
        """
        src = Path(src_path)
        dest = Path(dest_path)
        
        # Handle duplicate at destination
        if dest.exists():
            base = dest.stem
            suffix = dest.suffix
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            dest = dest.parent / f"{base}_{timestamp}{suffix}"
        
        # Move file
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dest))
        
        # Log action
        self.audit_logger.log_action(
            action_type='file_moved',
            file_path=str(dest),
            status='completed',
            metadata={
                'source_path': src_path,
                'destination_path': str(dest),
            }
        )
        
        print(f"[{self.name}] Moved: {src_path} → {dest}")
        return str(dest)
