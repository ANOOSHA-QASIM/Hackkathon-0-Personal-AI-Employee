# Python Sentinel Orchestration Skill

## Purpose
Expertise in developing Python 'Watchers' (Sentinel Scripts). Implements the BaseWatcher pattern for Gmail, WhatsApp (Playwright), and local file system monitoring to trigger Claude Code reasoning loops.

## Capabilities

### BaseWatcher Pattern
```python
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Dict, Any

class BaseWatcher(ABC):
    """Abstract base class for all Sentinel watchers."""
    
    def __init__(self, name: str, poll_interval_seconds: int = 60):
        self.name = name
        self.poll_interval = poll_interval_seconds
        self.last_check: Optional[datetime] = None
    
    @abstractmethod
    def check(self) -> list[Dict[str, Any]]:
        """Return list of triggered events."""
        pass
    
    @abstractmethod
    def transform_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Transform raw event into vault task format."""
        pass
    
    def run(self):
        """Main watcher loop."""
        while True:
            events = self.check()
            for event in events:
                task = self.transform_event(event)
                self.create_vault_task(task)
            self.last_check = datetime.now()
            time.sleep(self.poll_interval)
```

### Gmail Watcher Implementation
- Monitor Gmail via IMAP or Gmail API
- Filter rules: unread, specific labels, sender patterns
- Transform emails into vault tasks with metadata:
  - Subject → Task title
  - Sender → Context
  - Body → Task description
  - Labels → Tags
- Support attachments (save to `/attachments/`)

### WhatsApp Watcher (Playwright)
- Browser automation via Playwright for WhatsApp Web
- Monitor specific chats or keywords
- Extract message metadata:
  - Sender, timestamp, message content
  - Group vs individual chat detection
- Handle session persistence (cookies, local storage)
- Trigger on: mentions, keywords, unread messages

### Local Filesystem Watcher
- Use `watchdog` library for efficient file system events
- Monitor directories:
  - `/inbox/` - New files trigger processing
  - `/exports/` - Ready for sync
  - `/downloads/` - New data available
- Event types: created, modified, deleted, moved
- Debounce rapid changes (e.g., file writes in progress)

### Event Transformation Pipeline
```python
def transform_email_to_task(self, email_data: Dict) -> Dict:
    return {
        "title": f"Reply to: {email_data['subject']}",
        "folder": "Needs_Action",
        "frontmatter": {
            "status": "Needs_Action",
            "source": "gmail",
            "sender": email_data['from'],
            "received_at": email_data['date'].isoformat(),
            "message_id": email_data['id'],
            "tags": ["email", "reply", email_data['label']]
        },
        "content": f"""
## Context
From: {email_data['from']}
Subject: {email_data['subject']}
Date: {email_data['date']}

## Message
{email_data['body']}

## Attachments
{self._format_attachments(email_data.get('attachments', []))}
"""
    }
```

### Claude Code Trigger Integration
- On event detection, create task file in `/Needs_Action/`
- Optional: Send notification to trigger Claude Code loop
- Support webhook callbacks for external orchestration
- Log all events to `/logs/sentinel-{watcher_name}.log`

## Dependencies
```txt
watchdog>=3.0.0
playwright>=1.40.0
imaplib2>=3.0.0
google-auth-oauthlib>=1.0.0
python-dotenv>=1.0.0
```

## Configuration
```yaml
watchers:
  gmail:
    enabled: true
    poll_interval: 60
    labels: ["INBOX", "IMPORTANT"]
    exclude_senders: ["noreply@", "notifications@"]
  
  whatsapp:
    enabled: false
    poll_interval: 30
    monitored_chats: ["Project Team", "Boss"]
    keywords: ["urgent", "action required", "@me"]
  
  filesystem:
    enabled: true
    directories:
      - path: "./inbox"
        patterns: ["*.pdf", "*.md", "*.txt"]
```

## Error Handling
- Network failures: Exponential backoff, max 3 retries
- Session expired (WhatsApp): Notify user, pause watcher
- Parse errors: Log to audit, skip event, continue
- Vault write failures: Queue events in memory, retry on recovery

## Security
- Store credentials in `.env` (never commit)
- Use app-specific passwords for Gmail
- Encrypt WhatsApp session data
- Validate all file paths before write operations
