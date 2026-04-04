# Filesystem Management Skill

## Purpose
Expertise in managing Obsidian vault architecture. Handles `/Needs_Action`, `/In_Progress`, and `/Done` folders. Manages Markdown metadata, file-based state persistence, and claim-by-move rules for multi-agent synchronization.

## Capabilities

### Vault Structure Management
- Create and maintain standard Obsidian vault folders:
  - `/Needs_Action` - Incoming tasks requiring attention
  - `/In_Progress` - Active work items
  - `/Done` - Completed tasks (archived)
  - `/Approved` - Items awaiting execution (HITL gate)
- Enforce claim-by-move protocol: agents claim tasks by moving them to `/In_Progress`
- Prevent double-work through file-based locking (move semantics)

### Markdown Metadata Handling
- Parse and update YAML frontmatter in Markdown files
- Manage standard fields:
  - `status`: Needs_Action | In_Progress | Done | Approved
  - `assigned_to`: Agent identifier
  - `claimed_at`: ISO 8601 timestamp
  - `completed_at`: ISO 8601 timestamp
  - `tags`: Array of relevant tags
- Preserve user content while updating metadata

### File Operations
- Move files between vault folders atomically
- Create new Markdown files with proper frontmatter
- Archive completed items with timestamp preservation
- Handle file conflicts gracefully (rename on collision)

### Multi-Agent Synchronization
- Implement claim-by-move rules:
  1. Agent scans `/Needs_Action` for unclaimed tasks
  2. Agent moves task to `/In_Progress/{agent_name}/`
  3. Agent updates `assigned_to` and `claimed_at` in frontmatter
  4. On completion, move to `/Done/{YYYY-MM}/` for monthly archiving
- Prevent race conditions through atomic move operations
- Log all state changes for audit trail

## Usage Patterns

### Claiming a Task
```markdown
# Before (in /Needs_Action/)
---
status: Needs_Action
tags: [email, reply]
---

# After (moved to /In_Progress/email-agent/)
---
status: In_Progress
assigned_to: email-agent
claimed_at: 2026-03-28T10:30:00Z
tags: [email, reply]
---
```

### Completing a Task
```markdown
# Before (in /In_Progress/)
---
status: In_Progress
assigned_to: email-agent
claimed_at: 2026-03-28T10:30:00Z
---

# After (moved to /Done/2026-03/)
---
status: Done
assigned_to: email-agent
claimed_at: 2026-03-28T10:30:00Z
completed_at: 2026-03-28T11:15:00Z
---
```

## Integration Points
- **Sentinel Scripts**: Trigger vault scans for new tasks
- **HITL Compliance**: Respect `/Approved` gate for sensitive actions
- **Audit Logs**: Write to `/audit/{YYYY-MM-DD}.json` for all moves
- **Sync Infrastructure**: Coordinate with cloud-local sync to prevent conflicts

## Constraints
- Never modify files outside the vault structure
- Always preserve user content; only update frontmatter
- Atomic moves only; no partial state
- Log all operations for debugging

## Error Handling
- File exists at destination: Append timestamp to filename
- Frontmatter parse error: Log warning, preserve original, create `.error.md` copy
- Permission denied: Log to audit, skip file, continue processing
