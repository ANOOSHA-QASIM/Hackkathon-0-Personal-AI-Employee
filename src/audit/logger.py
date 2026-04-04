"""
Audit Logger for Digital FTE Vault.
Records all agent actions to daily JSON log files.
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from ..config.settings import LOGS_PATH


class AuditLogger:
    """Logger for recording agent actions to daily JSON files."""
    
    def __init__(self, agent_id: str):
        """
        Initialize audit logger.
        
        Args:
            agent_id: Unique identifier for the agent (e.g., 'filesystem-watcher')
        """
        self.agent_id = agent_id
        self.log_path: Optional[Path] = None
        self.log_data: Dict[str, Any] = {}
    
    def _get_today_log_path(self) -> Path:
        """Get path to today's log file."""
        today = datetime.now().strftime('%Y-%m-%d')
        return LOGS_PATH / f'{today}.json'
    
    def _initialize_log_file(self, log_path: Path) -> None:
        """Create new daily log file with initial structure."""
        today = datetime.now().strftime('%Y-%m-%d')
        self.log_data = {
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
        self._write_log_file(log_path)
    
    def _load_log_file(self, log_path: Path) -> None:
        """Load existing log file."""
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                self.log_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            self._initialize_log_file(log_path)
    
    def _write_log_file(self, log_path: Path) -> None:
        """Write log data to file."""
        LOGS_PATH.mkdir(parents=True, exist_ok=True)
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(self.log_data, f, indent=2)
    
    def log_action(
        self,
        action_type: str,
        file_path: str,
        status: str,
        metadata: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None
    ) -> None:
        """
        Log an action to today's audit file.
        
        Args:
            action_type: Type of action (file_detected, metadata_created, file_moved, error)
            file_path: Path to affected file
            status: Action status (pending, completed, blocked, error)
            metadata: Optional additional context
            error_message: Error details (required if status is 'error')
        """
        log_path = self._get_today_log_path()
        
        # Load or initialize log file
        if log_path.exists():
            self._load_log_file(log_path)
        else:
            self._initialize_log_file(log_path)
        
        # Create log entry
        entry = {
            'timestamp': datetime.now().isoformat() + 'Z',
            'action_type': action_type,
            'agent_id': self.agent_id,
            'file_path': file_path,
            'status': status,
        }
        
        # Add optional fields
        if metadata:
            entry['metadata'] = metadata
        if error_message:
            entry['error_message'] = error_message
        
        # Append entry
        self.log_data['entries'].append(entry)
        
        # Update summary
        self.log_data['summary'] = {
            'total_actions': len(self.log_data['entries']),
            'completed': sum(1 for e in self.log_data['entries'] if e['status'] == 'completed'),
            'errors': sum(1 for e in self.log_data['entries'] if e['status'] == 'error'),
        }
        
        # Write back
        self._write_log_file(log_path)
        self.log_path = log_path
    
    def seal_log(self) -> Dict[str, Any]:
        """
        Seal the current log file with SHA-256 hash.
        
        Returns:
            Seal metadata dictionary
        """
        if not self.log_path or not self.log_path.exists():
            raise FileNotFoundError("No log file to seal")
        
        # Read current content
        with open(self.log_path, 'r', encoding='utf-8') as f:
            content = self.log_data
        
        # Create hash (excluding seal fields)
        content_to_hash = {
            'date': content['date'],
            'vault_id': content['vault_id'],
            'entries': content['entries'],
            'summary': content['summary'],
        }
        content_hash = hashlib.sha256(
            json.dumps(content_to_hash, sort_keys=True).encode()
        ).hexdigest()
        
        # Update seal metadata
        self.log_data['sealed'] = True
        self.log_data['sealed_at'] = datetime.now().isoformat() + 'Z'
        self.log_data['content_hash'] = content_hash
        
        # Write sealed log
        self._write_log_file(self.log_path)
        
        return {
            'sealed_at': self.log_data['sealed_at'],
            'content_hash': content_hash,
            'entry_count': len(self.log_data['entries']),
        }


def create_initial_log(agent_id: str = 'system') -> None:
    """Create initial log entry for system initialization."""
    logger = AuditLogger(agent_id)
    logger.log_action(
        action_type='system_init',
        file_path=str(LOGS_PATH),
        status='completed',
        metadata={
            'message': 'Digital FTE Vault audit logging initialized',
            'phase': 1,
            'phase_name': 'Bronze: Foundation',
        }
    )
    print(f"[Audit] Initial log entry created at {logger.log_path}")
