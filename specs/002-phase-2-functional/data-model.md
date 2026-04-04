# Data Model: Phase 2 Functional

**Feature**: 002-phase-2-functional  
**Date**: 2026-03-28  
**Status**: Draft

## Overview

This document defines the core data entities for Phase 2 Functional (Gmail monitoring, LinkedIn posting, communication triage). All entities are file-based (Markdown with YAML frontmatter, JSON files) per the Constitution's file-based state persistence principle.

---

## Entity 1: EmailAlert

**Purpose**: YAML frontmatter schema for email alert files in `/Needs_Action`.

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `status` | string | ✅ | Alert state | `Needs_Action`, `In_Progress`, `Done` |
| `type` | string | ✅ | Source type | `email_alert` |
| `sender` | string | ✅ | Email sender address | `client@company.com` |
| `sender_name` | string | ❌ | Sender display name | `John Doe` |
| `subject` | string | ✅ | Email subject line | `Invoice #2026-001 Payment Required` |
| `received_timestamp` | string (ISO 8601) | ✅ | When email arrived | `2026-03-28T10:30:00Z` |
| `message_id` | string | ✅ | Gmail message ID (for deduplication) | `<abc123@mail.gmail.com>` |
| `priority` | string | ✅ | Priority level | `high`, `normal`, `low` |
| `tags` | array[string] | ❌ | Categorization tags | `["invoice", "accounting", "urgent"]` |
| `processed` | boolean | ✅ | Whether alert was processed | `false` |

### Example

```yaml
---
status: Needs_Action
type: email_alert
sender: client@company.com
sender_name: John Doe
subject: Invoice #2026-001 Payment Required
received_timestamp: 2026-03-28T10:30:00Z
message_id: <abc123@mail.gmail.com>
priority: high
tags:
  - invoice
  - accounting
  - urgent
processed: false
---

## Email Content

**From**: John Doe <client@company.com>
**Date**: 2026-03-28 10:30 AM

Hi,

Please find attached invoice #2026-001 for payment.

Best regards,
John
```

### Validation Rules

1. `status` MUST be one of: `Needs_Action`, `In_Progress`, `Approved`, `Rejected`, `Done`
2. `priority` MUST be one of: `high`, `normal`, `low`
3. `message_id` MUST be unique (used for deduplication)
4. If `priority` is `high`, then `tags` MUST include at least one high-priority tag
5. `processed` defaults to `false`; set to `true` when user responds to email

### State Transitions

```
Needs_Action → In_Progress (user claims email for response)
In_Progress → Done (email responded to)
Needs_Action → Done (email handled without claim)
```

---

## Entity 2: SocialMediaPost

**Purpose**: YAML frontmatter schema for social media post files in `/In_Progress`, `/Approved`, `/Done`.

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `status` | string | ✅ | Post state | `draft`, `approved`, `published`, `rejected` |
| `platform` | string | ✅ | Target platform | `linkedin`, `twitter`, `facebook` |
| `content` | string | ✅ | Post text content | `Excited to announce...` |
| `media_path` | string | ❌ | Path to image/media file | `./media/post-image.png` |
| `scheduled_time` | string (ISO 8601) | ❌ | When to publish | `2026-03-29T09:00:00Z` |
| `created_at` | string (ISO 8601) | ✅ | When draft created | `2026-03-28T14:00:00Z` |
| `created_by` | string | ✅ | Who created draft | `linkedin-agent` |
| `hitl_approved` | boolean | ✅ | HITL approval status | `false` |
| `hitl_approved_by` | string | ❌ | Who approved | `user` |
| `hitl_approved_at` | string (ISO 8601) | ❌ | When approved | `2026-03-28T15:00:00Z` |
| `published_at` | string (ISO 8601) | ❌ | When published | `2026-03-29T09:00:00Z` |
| `tags` | array[string] | ❌ | Post tags | `["announcement", "product-launch"]` |

### Example

```yaml
---
status: draft
platform: linkedin
content: |
  Excited to announce our new AI Employee automation system!
  
  This system combines Gmail monitoring, task management, and automated posting to help businesses scale efficiently.
  
  #Automation #AI #Productivity
media_path: ./media/announcement-dark.png
scheduled_time: 2026-03-29T09:00:00Z
created_at: 2026-03-28T14:00:00Z
created_by: linkedin-agent
hitl_approved: false
tags:
  - announcement
  - product-launch
  - automation
---

## Post Preview

**Platform**: LinkedIn
**Scheduled**: 2026-03-29 09:00 AM
**Media**: See attached image

---

## HITL Approval

- [ ] Approved (move to /Approved)
- [ ] Rejected (move to /Rejected with feedback)

**Feedback**: 
```

### Validation Rules

1. `status` MUST be one of: `draft`, `approved`, `published`, `rejected`, `scheduled`
2. `platform` MUST be one of: `linkedin`, `twitter`, `facebook`, `instagram`
3. If `media_path` is present, image MUST follow minimalist design rules (dark theme, clean typography)
4. If `scheduled_time` is present, post MUST be published within 2 minutes of scheduled time
5. `hitl_approved` MUST be `true` before publishing (enforced by LinkedIn publisher)
6. If `status` is `approved`, then `hitl_approved_by` and `hitl_approved_at` MUST be present

### State Transitions

```
draft → approved (user moves to /Approved)
approved → published (LinkedIn agent publishes)
draft → rejected (user moves to /Rejected)
rejected → draft (user revises and resubmits)
draft → scheduled (scheduled for future time)
scheduled → published (scheduled time arrives, auto-publish)
```

---

## Entity 3: CommunicationTriage

**Purpose**: Configuration for priority classification rules.

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `priority_keywords` | object | ✅ | Keywords by priority level | See below |
| `vip_senders` | array[string] | ✅ | VIP sender addresses | `["client@company.com"]` |
| `low_priority_domains` | array[string] | ❌ | Domains to mark as low priority | `["newsletter.com"]` |
| `updated_at` | string (ISO 8601) | ✅ | When rules last updated | `2026-03-28T00:00:00Z` |

### Example (YAML config file)

```yaml
# config/triage_rules.yaml
priority_keywords:
  high:
    - urgent
    - asap
    - invoice
    - payment
    - emergency
    - action required
    - overdue
  normal: []
  low:
    - newsletter
    - notification
    - update
    - digest
    - unsubscribe

vip_senders:
  - client@company.com
  - partner@business.com
  - boss@company.com

low_priority_domains:
  - newsletter.com
  - updates.social.com
  - notifications.github.com

updated_at: 2026-03-28T00:00:00Z
```

### Validation Rules

1. `priority_keywords.high` MUST have at least 3 keywords
2. `vip_senders` MUST have at least 1 sender
3. Keywords are case-insensitive (matched against lowercase subject)
4. VIP senders take precedence over keyword matching

---

## Entity 4: ProcessedEmails

**Purpose**: JSON log for tracking processed email message IDs (deduplication).

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `message_ids` | array[string] | ✅ | Set of processed Gmail message IDs | `["<abc123@mail.gmail.com>"]` |
| `last_updated` | string (ISO 8601) | ✅ | When log last updated | `2026-03-28T10:30:00Z` |

### Example

```json
{
  "message_ids": [
    "<abc123@mail.gmail.com>",
    "<def456@mail.gmail.com>",
    "<ghi789@mail.gmail.com>"
  ],
  "last_updated": "2026-03-28T10:30:00Z"
}
```

### Validation Rules

1. `message_ids` MUST be unique (no duplicates in array)
2. `last_updated` MUST be updated on each write
3. File MUST be stored in `/Logs/processed_emails.json`

---

## Entity 5: HITLGate

**Purpose**: Logical entity representing HITL approval workflow for LinkedIn posts.

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `approval_path` | string | ✅ | Folder path for approved items | `/Approved` |
| `rejection_path` | string | ✅ | Folder path for rejected items | `/Rejected` |
| `draft_path` | string | ✅ | Folder path for drafts | `/In_Progress/linkedin-agent` |
| `enforced` | boolean | ✅ | Whether gate is enforced | `true` |

### Validation Rules

1. `enforced` MUST be `true` (HITL is mandatory per Constitution Principle IV)
2. LinkedIn publisher MUST ONLY check `approval_path` for posts to publish
3. Posts in `draft_path` MUST NOT be published without moving to `approval_path`

---

## Relationships

```
EmailAlert
  ├── classified_by → CommunicationTriage (priority rules)
  ├── tracked_in → ProcessedEmails (deduplication)
  └── logged_in → AuditLogEntry (all actions recorded)

SocialMediaPost
  ├── created_by → LinkedInAgent (draft generator)
  ├── approved_via → HITLGate (folder-based approval)
  ├── published_by → LinkedInPublisher (Playwright)
  └── logged_in → AuditLogEntry (all actions recorded)

CommunicationTriage
  └── configured_by → User (VIP senders, keywords)

HITLGate
  └── enforced_by → Constitution Principle IV (mandatory)
```

---

## File Locations

| Entity | Storage Format | Location |
|--------|---------------|----------|
| EmailAlert | YAML frontmatter | `/Needs_Action/email-*.md` |
| SocialMediaPost | YAML frontmatter | `/In_Progress/linkedin-agent/*.md`, `/Approved/*.md`, `/Done/*.md` |
| CommunicationTriage | YAML config | `/config/triage_rules.yaml` |
| ProcessedEmails | JSON | `/Logs/processed_emails.json` |
| HITLGate | Logical (folder structure) | `/Approved`, `/Rejected`, `/In_Progress` |

---

## Schema Evolution

### Phase 2 (Current)
- EmailAlert: Basic fields (sender, subject, priority, message_id)
- SocialMediaPost: LinkedIn-only, manual scheduling, HITL approval
- CommunicationTriage: Keyword + VIP rules
- ProcessedEmails: Simple ID tracking

### Phase 3+ (Future)
- EmailAlert: Add `response_draft`, `responded_at` fields
- SocialMediaPost: Multi-platform support (Twitter, Facebook), auto-scheduling, engagement tracking
- CommunicationTriage: ML-based classification, user feedback loop
- ProcessedEmails: Add `processed_at`, `processing_agent` fields
