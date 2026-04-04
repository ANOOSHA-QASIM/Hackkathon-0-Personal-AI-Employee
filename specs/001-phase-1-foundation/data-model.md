# Data Model: Phase 1 Foundation

**Feature**: 001-phase-1-foundation  
**Date**: 2026-03-28  
**Status**: Draft

## Overview

This document defines the core data entities for Phase 1 Foundation. All entities are file-based (Markdown with YAML frontmatter, JSON files) per the Constitution's file-based state persistence principle.

---

## Entity 1: TaskMetadata

**Purpose**: YAML frontmatter schema for task files in `/Needs_Action` and `/In_Progress`.

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `status` | string | ✅ | Task state | `Needs_Action`, `In_Progress`, `Done` |
| `type` | string | ✅ | Source type | `file_drop`, `email`, `whatsapp`, `manual` |
| `original_name` | string | ✅ | Original filename (for file drops) | `invoice-2026-001.pdf` |
| `received_timestamp` | string (ISO 8601) | ✅ | When task entered system | `2026-03-28T10:30:00Z` |
| `assigned_to` | string | ❌ | Agent claiming task | `email-agent` |
| `claimed_at` | string (ISO 8601) | ❌ | When task was claimed | `2026-03-28T11:00:00Z` |
| `completed_at` | string (ISO 8601) | ❌ | When task was completed | `2026-03-28T11:30:00Z` |
| `tags` | array[string] | ❌ | Categorization tags | `["invoice", "payment", "urgent"]` |
| `priority` | string | ❌ | Task priority | `urgent`, `normal`, `low` |

### Example

```yaml
---
status: Needs_Action
type: file_drop
original_name: invoice-2026-001.pdf
received_timestamp: 2026-03-28T10:30:00Z
tags:
  - invoice
  - payment
priority: normal
---

## Task Description

Process invoice for payment approval.
```

### Validation Rules

1. `status` MUST be one of: `Needs_Action`, `In_Progress`, `Approved`, `Rejected`, `Done`
2. `received_timestamp` MUST be valid ISO 8601 format
3. `type` MUST be one of: `file_drop`, `email`, `whatsapp`, `linkedin`, `manual`
4. If `status` is `In_Progress`, then `assigned_to` and `claimed_at` MUST be present
5. If `status` is `Done`, then `completed_at` MUST be present

### State Transitions

```
Needs_Action → In_Progress (claim by agent)
In_Progress → Approved (ready for HITL)
Approved → In_Progress (HITL approved, execute)
Approved → Rejected (HITL rejected)
In_Progress → Done (completion)
Rejected → Needs_Action (rework)
```

---

## Entity 2: AuditLogEntry

**Purpose**: Schema for entries in `/Logs/YYYY-MM-DD.json`.

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `timestamp` | string (ISO 8601) | ✅ | When action occurred | `2026-03-28T10:30:00Z` |
| `action_type` | string | ✅ | Type of action | `file_detected`, `metadata_created`, `file_moved`, `error` |
| `agent_id` | string | ✅ | Which agent performed action | `filesystem-watcher` |
| `file_path` | string | ✅ | Affected file path | `/Inbox/invoice.pdf` |
| `status` | string | ✅ | Action result | `pending`, `completed`, `blocked`, `error` |
| `metadata` | object | ❌ | Additional context | `{"original_name": "invoice.pdf"}` |
| `error_message` | string | ❌ | Error details (if status=error) | `Permission denied` |

### Example

```json
{
  "timestamp": "2026-03-28T10:30:00Z",
  "action_type": "file_detected",
  "agent_id": "filesystem-watcher",
  "file_path": "/Inbox/invoice-2026-001.pdf",
  "status": "completed",
  "metadata": {
    "original_name": "invoice-2026-001.pdf",
    "size_bytes": 45678
  }
}
```

### Validation Rules

1. `timestamp` MUST be valid ISO 8601 format
2. `action_type` MUST be one of: `file_detected`, `metadata_created`, `file_moved`, `task_created`, `error`, `dashboard_updated`, `handbook_updated`
3. `status` MUST be one of: `pending`, `completed`, `blocked`, `error`
4. If `status` is `error`, then `error_message` MUST be present
5. Entries MUST be appended (never modified) after creation

### Daily Log Structure

```json
{
  "date": "2026-03-28",
  "vault_id": "AI_Employee_vault",
  "entries": [
    {...},
    {...}
  ],
  "summary": {
    "total_actions": 15,
    "completed": 14,
    "errors": 1
  },
  "sealed": false,
  "sealed_at": null,
  "content_hash": null
}
```

---

## Entity 3: DashboardSection

**Purpose**: Structure definition for sections in `Dashboard.md`.

### Sections

#### 3.1: Bank Balance Section

| Field | Type | Required | Description | Phase |
|-------|------|----------|-------------|-------|
| `current_balance` | number | ✅ | Current balance in USD | 1 (manual) |
| `currency` | string | ✅ | Currency code | `USD` |
| `last_updated` | string (ISO 8601) | ✅ | Last manual/automatic update | 1 (manual) |
| `last_transaction_date` | string (date) | ❌ | Date of most recent transaction | 2+ (auto) |

**Phase 1 Format** (Manual):
```markdown
## Bank Balance

- **Current Balance**: $5,432.10 USD
- **Last Updated**: 2026-03-28 09:00 AM
- **Last Transaction**: 2026-03-27 (Invoice Payment - $1,500.00)
```

#### 3.2: Pending Messages Section

| Field | Type | Required | Description | Phase |
|-------|------|----------|-------------|-------|
| `gmail_unread_count` | integer | ✅ | Unread Gmail messages | 1 (manual) |
| `whatsapp_unread_count` | integer | ✅ | Unread WhatsApp messages | 1 (manual) |
| `last_checked` | string (ISO 8601) | ✅ | Last refresh timestamp | 1 (manual) |

**Phase 1 Format** (Manual):
```markdown
## Pending Messages

- **Gmail**: 12 unread
- **WhatsApp**: 5 unread
- **Last Checked**: 2026-03-28 10:30 AM
```

#### 3.3: Active Projects Section

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `project_name` | string | ✅ | Project display name |
| `status` | string | ✅ | Current status |
| `next_action` | string | ✅ | Next concrete step |
| `last_updated` | string (date) | ❌ | Last status update |

**Status Values**: `In_Progress`, `Waiting`, `Blocked`, `Completed`

**Phase 1 Format** (Manual):
```markdown
## Active Projects

| Project | Status | Next Action | Last Updated |
|---------|--------|-------------|--------------|
| Website Redesign | In_Progress | Review mockups | 2026-03-27 |
| Q1 Tax Filing | Waiting | Wait for accountant | 2026-03-25 |
| Client Onboarding | In_Progress | Send welcome email | 2026-03-28 |
```

---

## Entity 4: HandbookRule

**Purpose**: Structure for rules in `Company_Handbook.md`.

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `rule_id` | string | ✅ | Unique identifier | `RULE-001` |
| `category` | string | ✅ | Rule category | `priority`, `escalation`, `communication` |
| `title` | string | ✅ | Short descriptive title | `Payment Escalation` |
| `description` | string | ✅ | Detailed rule description | See below |
| `examples` | array[string] | ❌ | Example scenarios | `["Invoice > $500 requires approval"]` |

### Example

```markdown
### RULE-001: Payment Escalation

**Category**: Escalation

**Description**: All payments exceeding $500 USD MUST be moved to /Approved for human review before processing. Payments ≤ $500 may be processed autonomously if invoice matches purchase order.

**Examples**:
- Invoice $450 → Process autonomously
- Invoice $750 → Move to /Approved with justification
```

### Categories

1. **Priority**: Task prioritization rules (urgent vs normal vs low)
2. **Escalation**: When to escalate to human (HITL triggers)
3. **Communication**: Tone, style, branding guidelines
4. **Workflow**: Process rules (claim-by-move, audit logging)
5. **Security**: Credential handling, data protection

---

## Entity 5: WatcherConfig

**Purpose**: Configuration for watcher instances (FileSystem, Gmail, etc.).

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `name` | string | ✅ | Watcher identifier | `filesystem-watcher` |
| `enabled` | boolean | ✅ | Whether watcher is active | `true` |
| `poll_interval` | integer | ✅ | Check interval in seconds | `60` |
| `source_path` | string | ❌ | Monitored directory (for file watcher) | `/Inbox` |
| `batch_size` | integer | ❌ | Max items per processing cycle | `10` |

### Example

```yaml
watchers:
  - name: filesystem-watcher
    enabled: true
    poll_interval: 60
    source_path: E:/hackathon_0_digital_fte/AI_Employee_vault/Inbox
    batch_size: 10
  
  - name: gmail-watcher
    enabled: false  # Phase 2
    poll_interval: 60
    batch_size: 20
```

---

## Relationships

```
TaskMetadata
  ├── created_by → WatcherConfig (which watcher created the task)
  ├── assigned_to → Agent (which agent claimed it)
  └── logged_in → AuditLogEntry (all actions recorded)

DashboardSection
  ├── populated_by → Agent (manual or automated)
  └── updated_from → TaskMetadata (for Active Projects)

HandbookRule
  └── enforced_by → Agent (agents check rules during execution)

AuditLogEntry
  ├── performed_by → Agent
  └── affects → TaskMetadata (file_path reference)
```

---

## File Locations

| Entity | Storage Format | Location |
|--------|---------------|----------|
| TaskMetadata | YAML frontmatter | `/Needs_Action/*.md`, `/In_Progress/*/*.md` |
| AuditLogEntry | JSON | `/Logs/YYYY-MM-DD.json` |
| DashboardSection | Markdown | `/Dashboard.md` |
| HandbookRule | Markdown | `/Company_Handbook.md` |
| WatcherConfig | YAML | `/.env` or `/config/watchers.yaml` |

---

## Schema Evolution

### Phase 1 (Current)
- TaskMetadata: Basic fields (status, type, original_name, timestamp)
- AuditLogEntry: Core fields (timestamp, action_type, agent_id, file_path, status)
- DashboardSection: Manual entry format
- HandbookRule: Static Markdown format

### Phase 2+ (Future)
- TaskMetadata: Add `source_channel` (email address, phone number)
- AuditLogEntry: Add `hitl_approved_by` (human approver ID)
- DashboardSection: Auto-populated from APIs
- WatcherConfig: Add authentication fields (OAuth tokens, API keys)
