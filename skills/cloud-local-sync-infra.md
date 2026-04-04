# Cloud-Local Sync Infrastructure Skill

## Purpose
Infrastructure skill for Platinum-tier synchronization. Manages Git/Syncthing logic between Cloud VMs and Local machines, enforcing strict permission boundaries and preventing double-work.

## Capabilities

### Sync Architecture
```
┌─────────────────┐                    ┌─────────────────┐
│   Cloud VM      │                    │  Local Machine  │
│  (Always On)    │◄──── Sync ────────►│   (Workstation) │
│                 │                    │                 │
│ /vault/         │                    │ /vault/         │
│   /Needs_Action │                    │   /Needs_Action │
│   /In_Progress  │                    │   /In_Progress  │
│   /Done         │                    │   /Done         │
│   /Approved     │                    │   /Approved     │
│   /audit/       │                    │   /audit/       │
└─────────────────┘                    └─────────────────┘
         │                                      │
         │         ┌──────────────┐             │
         └────────►│  Sync State  │◄────────────┘
                   │  (Git/Sync)  │
                   └──────────────┘
```

### Sync Method Comparison
| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| Git | Version history, conflict detection, branching | Manual commits/pushes, merge conflicts | Audit trail, backup |
| Syncthing | Real-time, automatic, bidirectional | No version history, potential conflicts | Active work sync |
| Hybrid | Best of both | Complex setup | Platinum tier |

### Git Sync Implementation
```python
import git
from datetime import datetime
from typing import Optional

class VaultGitSync:
    def __init__(self, vault_path: str, remote_url: str, ssh_key_path: str):
        self.vault_path = vault_path
        self.remote_url = remote_url
        self.ssh_key_path = ssh_key_path
        self.repo = git.Repo(vault_path)
        self._configure_ssh()
    
    def _configure_ssh(self):
        """Configure SSH for Git operations."""
        ssh_cmd = f"ssh -i {self.ssh_key_path}"
        self.repo.git.custom_environment(GIT_SSH_COMMAND=ssh_cmd)
    
    def sync_to_cloud(self, message: str = "Auto-sync from local") -> Dict:
        """Push local changes to cloud VM."""
        # Check for uncommitted changes
        if self.repo.is_dirty():
            # Auto-commit vault state
            self.repo.git.add(A=True)
            self.repo.git.commit(m=f"{message} - {datetime.now().isoformat()}")
        
        # Pull latest from cloud
        try:
            self.repo.git.pull("origin", "main")
        except git.GitCommandError as e:
            # Handle merge conflicts
            return self._handle_conflict(e)
        
        # Push local changes
        result = self.repo.git.push("origin", "main")
        
        return {
            "status": "success",
            "synced_at": datetime.now().isoformat(),
            "direction": "local_to_cloud",
            "result": result
        }
    
    def sync_from_cloud(self) -> Dict:
        """Pull latest from cloud VM."""
        # Stash local changes if any
        had_local_changes = self.repo.is_dirty()
        if had_local_changes:
            self.repo.git.stash("save", "WIP local changes")
        
        # Pull from cloud
        try:
            self.repo.git.pull("origin", "main")
            result = {"status": "success"}
        except git.GitCommandError as e:
            # Restore stash on conflict
            if had_local_changes:
                self.repo.git.stash("pop")
            result = self._handle_conflict(e)
        
        return {
            **result,
            "synced_at": datetime.now().isoformat(),
            "direction": "cloud_to_local"
        }
    
    def _handle_conflict(self, error: git.GitCommandError) -> Dict:
        """Handle merge conflicts gracefully."""
        # Log conflict details
        conflict_files = self._get_conflicted_files()
        
        # Create conflict report
        return {
            "status": "conflict",
            "error": str(error),
            "conflicted_files": conflict_files,
            "resolution_required": True,
            "auto_resolved": False
        }
    
    def _get_conflicted_files(self) -> list:
        """List files with merge conflicts."""
        conflicted = []
        for item in self.repo.index.entries.values():
            path = item[0]
            full_path = f"{self.vault_path}/{path}"
            try:
                with open(full_path, 'r') as f:
                    content = f.read()
                    if "<<<<<<<" in content:
                        conflicted.append(path)
            except:
                pass
        return conflicted
```

### Syncthing Implementation
```python
import requests
from typing import Dict, List

class SyncthingClient:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url.rstrip('/')
        self.api_key = api_key
        self.headers = {"X-API-Key": api_key}
    
    def get_status(self) -> Dict:
        """Get Syncthing daemon status."""
        response = requests.get(
            f"{self.api_url}/rest/system/status",
            headers=self.headers
        )
        return response.json()
    
    def get_connections(self) -> Dict:
        """Get peer connections."""
        response = requests.get(
            f"{self.api_url}/rest/system/connections",
            headers=self.headers
        )
        return response.json()
    
    def get_folder_status(self, folder_id: str) -> Dict:
        """Get status of specific folder."""
        response = requests.get(
            f"{self.api_url}/rest/db/status?folder={folder_id}",
            headers=self.headers
        )
        return response.json()
    
    def scan_folder(self, folder_id: str) -> Dict:
        """Trigger folder scan."""
        response = requests.post(
            f"{self.api_url}/rest/db/scan?folder={folder_id}",
            headers=self.headers
        )
        return response.json()
    
    def get_pending_changes(self, folder_id: str) -> List[Dict]:
        """Get list of pending changes to sync."""
        response = requests.get(
            f"{self.api_url}/rest/db/need?folder={folder_id}",
            headers=self.headers
        )
        data = response.json()
        return data.get('progress', []) + data.get('received', [])
```

### Double-Work Prevention Protocol
```python
from enum import Enum

class SyncState(Enum):
    SYNCED = "synced"
    LOCAL_ONLY = "local_only"
    CLOUD_ONLY = "cloud_only"
    CONFLICT = "conflict"
    LOCKED = "locked"

class DoubleWorkPreventor:
    def __init__(self, vault_path: str, sync_method: str = "hybrid"):
        self.vault_path = vault_path
        self.sync_method = sync_method
        self.lock_file = f"{vault_path}/.sync_lock"
    
    def claim_file(self, file_path: str, agent: str) -> bool:
        """Claim a file for editing, preventing double-work."""
        lock_path = f"{file_path}.lock"
        
        # Check if already locked
        if self._is_locked(file_path):
            return False
        
        # Create lock file
        self._create_lock(file_path, agent)
        
        return True
    
    def release_file(self, file_path: str) -> bool:
        """Release file lock after editing."""
        lock_path = f"{file_path}.lock"
        
        if os.path.exists(lock_path):
            os.remove(lock_path)
            return True
        return False
    
    def _is_locked(self, file_path: str) -> bool:
        lock_path = f"{file_path}.lock"
        return os.path.exists(lock_path)
    
    def _create_lock(self, file_path: str, agent: str):
        lock_path = f"{file_path}.lock"
        with open(lock_path, 'w') as f:
            json.dump({
                "locked_by": agent,
                "locked_at": datetime.now().isoformat(),
                "reason": "editing"
            }, f, indent=2)
    
    def get_sync_state(self) -> SyncState:
        """Determine current sync state."""
        if self.sync_method == "git":
            return self._get_git_sync_state()
        elif self.sync_method == "syncthing":
            return self._get_syncthing_sync_state()
        else:
            return self._get_hybrid_sync_state()
    
    def _get_git_sync_state(self) -> SyncState:
        repo = git.Repo(self.vault_path)
        
        if repo.is_dirty():
            return SyncState.LOCAL_ONLY
        
        # Check if behind remote
        repo.git.fetch("origin", "main")
        local_commit = repo.head.commit.hexsha
        remote_commit = repo.commit("origin/main").hexsha
        
        if local_commit != remote_commit:
            return SyncState.CLOUD_ONLY
        
        return SyncState.SYNCED
```

### Permission Boundaries
```yaml
# Permission matrix for sync
permissions:
  cloud_vm:
    read:
      - /Needs_Action/**
      - /In_Progress/**
      - /Done/**
      - /audit/**
    write:
      - /Needs_Action/**
      - /In_Progress/**
      - /Done/**
      - /audit/**
    execute:
      - sentinel scripts
      - MCP servers
  
  local_machine:
    read:
      - /Needs_Action/**
      - /In_Progress/**
      - /Done/**
      - /audit/**
    write:
      - /In_Progress/**  # Only claimed files
      - /audit/**
    execute:
      - user interactions
      - browser automation
  
  shared:
    # Files both can modify (with locking)
    - /In_Progress/**
    
    # Read-only for both (append-only for audit)
    - /Done/**
    - /audit/**
```

### Conflict Resolution Strategy
```python
def resolve_sync_conflict(conflict: Dict) -> Dict:
    """Resolve sync conflicts with strategy."""
    strategy = conflict.get('type')
    
    if strategy == "both_modified":
        # Use timestamp-based resolution
        if conflict['local_mtime'] > conflict['cloud_mtime']:
            return {"winner": "local", "action": "overwrite_cloud"}
        else:
            return {"winner": "cloud", "action": "overwrite_local"}
    
    elif strategy == "both_created":
        # Create conflict copy, notify user
        return {
            "winner": "manual",
            "action": "create_conflict_copy",
            "files": [
                conflict['path'] + ".local",
                conflict['path'] + ".cloud"
            ]
        }
    
    elif strategy == "deleted_vs_modified":
        # Modified wins (safer)
        return {
            "winner": "modified",
            "action": "restore_modified"
        }
    
    return {"winner": "manual", "action": "user_decision"}
```

### Configuration
```yaml
sync:
  method: hybrid  # git | syncthing | hybrid
  
  git:
    remote_url: "git@github.com:user/ai-vault.git"
    branch: main
    ssh_key: "~/.ssh/cloud_vm"
    auto_commit: true
    commit_message_prefix: "[Auto-Sync]"
    push_on_change: false  # Manual trigger recommended
  
  syncthing:
    api_url: "http://localhost:8384"
    api_key: "${SYNCTHING_API_KEY}"
    folder_id: "ai-vault-sync"
    scan_interval: 60  # seconds
  
  conflict_resolution:
    strategy: timestamp  # timestamp | manual | merge
    notify_on_conflict: true
    backup_before_overwrite: true
  
  locking:
    enabled: true
    timeout_minutes: 30  # Auto-release stale locks
```

### Error Handling
- Network failure: Queue changes, retry on reconnect
- Conflict detected: Create backup, notify user, pause sync
- Lock timeout: Auto-release locks older than threshold
- Permission denied: Log error, skip file, continue
- Disk full: Alert user, pause sync, cleanup old backups

### Security
- SSH keys with passphrase protection
- Syncthing API key in `.env`
- Encrypted sync traffic (TLS for Syncthing)
- Access control: Only authenticated peers
- Audit all sync operations
