# Technical Research: Phase 1 Foundation

**Feature**: 001-phase-1-foundation  
**Date**: 2026-03-28  
**Status**: Complete

## Research Summary

This document resolves all technical unknowns identified during plan creation. Each section includes the decision made, rationale, and alternatives considered.

---

## 1. File System Monitoring Pattern

**Question**: What is the best approach for monitoring the /Inbox directory for new files?

### Decision
Use the **`watchdog`** library (v3.0.0+) for cross-platform file system event monitoring.

### Rationale
- **Efficiency**: Uses OS-level APIs (ReadDirectoryChangesW on Windows, inotify on Linux, FSEvents on macOS) instead of polling
- **Event-driven**: Receives immediate notifications when files are created, modified, or deleted
- **Debouncing support**: Can filter out rapid successive events (e.g., file write in progress)
- **Cross-platform**: Works consistently across Windows, macOS, and Linux
- **Well-maintained**: Active development, good documentation, widely adopted

### Implementation Pattern
```python
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class InboxHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            process_new_file(event.src_path)

observer = Observer()
observer.schedule(InboxHandler(), path='/Inbox', recursive=False)
observer.start()
```

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Polling (os.listdir every N seconds) | Simple, no dependencies | Inefficient, delayed detection, CPU waste | Violates <60s detection requirement |
| Windows API (ReadDirectoryChangesW) | Native, fastest | Windows-only, complex setup | Not portable, over-engineered |
| `watchfiles` (async alternative) | Async-native, modern | Newer, less battle-tested | watchdog is more mature for this use case |

---

## 2. YAML Frontmatter Parsing

**Question**: How should we parse and generate YAML frontmatter in Markdown files?

### Decision
Use **`pyyaml`** (v6.0+) for YAML parsing and generation.

### Rationale
- **Standard library**: De facto standard for YAML in Python
- **Robust**: Handles edge cases (multiline strings, special characters, dates)
- **Simple API**: `yaml.safe_load()` and `yaml.dump()` for most operations
- **Safe**: `safe_load` prevents arbitrary code execution from untrusted YAML
- **Well-documented**: Extensive examples and community support

### Implementation Pattern
```python
import yaml

def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from Markdown content."""
    if content.startswith('---'):
        end = content.find('---', 3)
        yaml_content = content[3:end].strip()
        return yaml.safe_load(yaml_content)
    return {}

def generate_frontmatter(metadata: dict) -> str:
    """Generate YAML frontmatter string."""
    return '---\n' + yaml.dump(metadata, sort_keys=False) + '---\n'
```

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Manual string parsing | No dependencies | Error-prone, breaks on edge cases | Not maintainable, violates reliability |
| `ruamel.yaml` | Preserves comments, round-trip | Overkill for simple frontmatter | Added complexity not needed |
| `toml` | Cleaner syntax | Not standard for Markdown frontmatter | Ecosystem convention favors YAML |

---

## 3. Audit Log Schema Design

**Question**: What schema should audit logs follow for compliance and extensibility?

### Decision
Use **JSON Schema** with required fields: `timestamp`, `action_type`, `agent_id`, `file_path`, `status`.

### Rationale
- **Machine-readable**: Easy to parse, query, and aggregate
- **Extensible**: Can add optional fields without breaking existing consumers
- **Validatable**: JSON Schema enables automated validation
- **Standard format**: Interoperable with logging/monitoring tools
- **Supports sealing**: Hash can be appended to final entry for integrity

### Schema Definition
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["timestamp", "action_type", "agent_id", "file_path", "status"],
  "properties": {
    "timestamp": {"type": "string", "format": "date-time"},
    "action_type": {"type": "string", "enum": ["file_detected", "metadata_created", "file_moved", "error"]},
    "agent_id": {"type": "string"},
    "file_path": {"type": "string"},
    "status": {"type": "string", "enum": ["pending", "completed", "blocked", "error"]},
    "metadata": {"type": "object"},
    "error_message": {"type": "string"}
  }
}
```

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| CSV | Simple, spreadsheet-friendly | Not extensible, hard to nest data | Violates extensibility requirement |
| Markdown table | Human-readable | Hard to parse programmatically | Violates machine-readable requirement |
| SQLite database | Queryable, structured | Overkill for simple logging, requires DB driver | Added complexity not needed for Phase 1 |

---

## 4. Duplicate File Handling Strategy

**Question**: How should the system handle files with identical names dropped into /Inbox?

### Decision
**Append timestamp to metadata `original_name` field**, not the actual filename. Each processed file gets a unique destination filename in /Needs_Action with format: `YYYYMMDD_HHMMSS_{sanitized_original_name}.md`

### Rationale
- **Preserves original filename**: User can see what the file was originally called
- **Prevents data loss**: Every file gets unique processing
- **Chronological ordering**: Timestamp prefix enables sorting by arrival time
- **Clear audit trail**: Metadata links back to original filename

### Implementation Pattern
```python
from datetime import datetime

def generate_unique_filename(original_name: str) -> str:
    """Generate unique filename with timestamp prefix."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    sanitized = original_name.replace(' ', '_').replace('.md', '')
    return f"{timestamp}_{sanitized}.md"

def process_file(src_path: str):
    original_name = os.path.basename(src_path)
    dest_name = generate_unique_filename(original_name)
    metadata = {
        'status': 'Needs_Action',
        'type': 'file_drop',
        'original_name': original_name,  # Preserve original
        'received_timestamp': datetime.now().isoformat(),
    }
    # Write to /Needs_Action/{dest_name} with metadata
```

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Overwrite existing file | Simple | **DATA LOSS** | Unacceptable |
| Skip duplicate files | Simple, safe | User confusion, lost work | Violates "process all files" requirement |
| Append number suffix (file_1, file_2) | Prevents collision | Doesn't preserve timing info | Timestamp is more informative |
| Move to /Inbox/conflicts/ | Safe, visible | Requires manual resolution | Adds friction, delays processing |

---

## 5. Dashboard Update Strategy

**Question**: How should the Dashboard.md be populated with real-time data in Phase 1?

### Decision
**Manual update in Phase 1** with placeholder/static data. Automation deferred to Phase 2+ when external integrations (Gmail API, bank APIs) are available.

### Rationale
- **Phase 1 scope**: Constitution Principle V (Strict Phase Lock) prohibits Phase 2+ features
- **External dependencies**: Gmail, WhatsApp, and bank integrations require API setup (Phase 2)
- **Early value**: Dashboard structure can be validated even with manual data
- **Clear upgrade path**: Phase 2 replaces manual sections with automated queries

### Phase 1 Dashboard Structure
```markdown
# Business Dashboard

## Bank Balance
- **Current Balance**: $X,XXX.XX (manual entry)
- **Last Updated**: YYYY-MM-DD HH:MM (manual)

## Pending Messages
- **Gmail**: X unread (manual count)
- **WhatsApp**: X unread (manual count)

## Active Projects
- Project A: Status - In Progress, Next: [task]
- Project B: Status - Waiting, Next: [task]
```

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Mock/fake data only | Fully automated | Misleading, not trustworthy | Violates SC-002 (accurate reflection) |
| Delay dashboard to Phase 2 | Clean implementation | Reduces Phase 1 value | Dashboard is P1 priority per spec |
| Partial automation (file counts only) | Some automation | Still requires manual for bank/messages | Consistency: all manual or all auto |

---

## 6. BaseWatcher Pattern Design

**Question**: What is the optimal class hierarchy for watchers (FileSystem, Gmail, WhatsApp, etc.)?

### Decision
Implement **abstract `BaseWatcher` class** with common functionality. All watchers (FileSystem, Gmail, WhatsApp) inherit from this base.

### Rationale
- **Code reuse**: Common logic (logging, metadata generation, error handling) in base class
- **Consistent interface**: All watchers implement `check()` and `transform_event()` methods
- **Extensibility**: New watchers (Phase 2+) follow same pattern
- **Testability**: Base class can be unit tested independently

### Class Hierarchy
```python
from abc import ABC, abstractmethod

class BaseWatcher(ABC):
    def __init__(self, name: str, poll_interval: int = 60):
        self.name = name
        self.poll_interval = poll_interval
    
    @abstractmethod
    def check(self) -> list:
        """Detect new events/items."""
        pass
    
    @abstractmethod
    def transform_event(self, event: dict) -> dict:
        """Convert event to task metadata."""
        pass
    
    def log_action(self, action_type: str, file_path: str, status: str):
        """Write to audit log."""
        write_audit_entry(action_type, self.name, file_path, status)

class FileSystemWatcher(BaseWatcher):
    def check(self) -> list:
        # Watchdog event handling
        pass
    
    def transform_event(self, event: dict) -> dict:
        # File-specific metadata
        pass
```

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Single monolithic watcher | Simple initially | Hard to extend, violates SRP | Won't scale to Phase 2+ watchers |
| Functional approach (no classes) | Lightweight | Less structure, harder to maintain | OOP pattern better for extensibility |
| Separate unrelated watchers | Independent | Code duplication, inconsistent interfaces | BaseWatcher ensures consistency |

---

## Conclusion

All technical unknowns resolved. Key decisions:
1. **watchdog** for file monitoring (efficient, event-driven)
2. **pyyaml** for frontmatter (standard, robust)
3. **JSON Schema** for audit logs (extensible, validatable)
4. **Timestamp-prefixed filenames** for duplicates (prevents data loss)
5. **Manual dashboard** in Phase 1 (defers external integrations to Phase 2)
6. **BaseWatcher pattern** for extensibility (consistent watcher interface)

Proceed to Phase 1: Generate data-model.md, contracts, and quickstart.md.
