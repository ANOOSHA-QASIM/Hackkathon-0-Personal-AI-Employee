# Implementation Plan: Phase 2 Functional - External Communication Senses

**Branch**: `002-phase-2-functional` | **Date**: 2026-03-28 | **Spec**: [specs/002-phase-2-functional/spec.md](../spec.md)

**Input**: Implement Gmail monitoring and LinkedIn posting infrastructure with HITL workflow.

## Summary

Build Phase 2 Functional layer adding external communication capabilities to the Digital FTE system. Implements Gmail API monitoring for unread emails (creating alerts in `/Needs_Action`), LinkedIn post workflow with HITL approval (draft in `/In_Progress`, approve in `/Approved`, publish via Playwright), communication triage for priority categorization, and social media metadata schema for structured post management. All components follow Constitution principles including HITL gates, audit logging, and minimalist design.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: 
- google-auth-oauthlib (Gmail API authentication)
- google-api-python-client (Gmail API client)
- playwright (LinkedIn browser automation)
- pyyaml (metadata parsing)
- python-dotenv (environment config)
**Storage**: File-based (Markdown files with YAML frontmatter, JSON credentials, audit logs)
**Testing**: pytest for unit tests, integration tests for Gmail/LinkedIn workflows
**Target Platform**: Windows (E:/ drive local filesystem)
**Project Type**: Single Python service with file-based state management, external API integrations
**Performance Goals**: 
- Gmail check every 5 minutes
- Email alerts created within 5 minutes of arrival
- LinkedIn posts published within 10 minutes of approval
- 90% priority classification accuracy
**Constraints**: 
- HITL mandatory for all LinkedIn posts (Constitution Principle IV)
- Minimalist design for image posts (Constitution Principle VII)
- Use credentials.json from Phase 1
- All actions logged to /Logs/YYYY-MM-DD.json
**Scale/Scope**: 
- Single Gmail account monitoring
- Single LinkedIn account posting
- 50+ emails/day processing
- 5-10 posts/week scheduling

## Constitution Check

**GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.**

| Principle | Compliance | Notes |
|-----------|------------|-------|
| I. Inbox-First Data Entry | ✅ PASS | Gmail emails enter via watcher → /Needs_Action with metadata |
| II. Needs_Action Schema Compliance | ✅ PASS | Email alerts and post drafts include YAML frontmatter |
| III. Claim-By-Move Protocol | ✅ PASS | LinkedIn agent claims posts by moving to /In_Progress/linkedin-agent/ |
| IV. HITL Mandatory for External Actions | ✅ PASS | LinkedIn posts require /Approved before publishing (enforced gate) |
| V. Strict Phase Lock | ✅ PASS | This is Phase 2; Phase 1 Foundation is complete |
| VI. Audit Logging | ✅ PASS | All Gmail/LinkedIn actions logged to /Logs/YYYY-MM-DD.json |
| VII. Minimalist Design | ✅ PASS | Image posts enforce dark theme, clean typography, no human icons |

**GATE RESULT**: ✅ PASS - All principles satisfied. Proceed to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/002-phase-2-functional/
├── plan.md              # This file
├── research.md          # Phase 0 output (Gmail/LinkedIn API research)
├── data-model.md        # Phase 1 output (email alert, post schemas)
├── quickstart.md        # Phase 1 output (setup guide)
└── contracts/           # Phase 1 output (metadata schemas)
    ├── email-alert-schema.yaml
    └── social-media-post-schema.yaml
```

### Source Code (repository root)

```text
src/
├── gmail/
│   ├── __init__.py
│   ├── gmail_watcher.py      # Gmail API monitoring
│   ├── email_processor.py    # Convert emails to alerts
│   └── triage.py             # Priority classification
├── linkedin/
│   ├── __init__.py
│   ├── post_generator.py     # Draft post creation
│   ├── linkedin_publisher.py # Playwright-based posting
│   └── scheduler.py          # Scheduled post execution
├── triage/
│   ├── __init__.py
│   └── communication_triage.py # Unified priority logic
└── config/
    └── settings.py           # Environment configuration (extends Phase 1)

tests/
├── contract/
│   ├── test_email_schema.py
│   └── test_post_schema.py
├── integration/
│   ├── test_gmail_flow.py
│   └── test_linkedin_workflow.py
└── unit/
    ├── test_gmail_watcher.py
    ├── test_triage.py
    └── test_post_generator.py
```

**Structure Decision**: Single Python project structure extending Phase 1. New modules (gmail/, linkedin/, triage/) follow same patterns as Phase 1 (watcher/, audit/, dashboard/).

## Complexity Tracking

No violations. All design decisions align with Constitution principles.

## Phase 0: Research & Technical Decisions

### Research Tasks Completed

1. **Gmail API Integration Pattern**
   - Decision: Use `google-api-python-client` with OAuth2 credentials (credentials.json)
   - Rationale: Official Google library, well-documented, supports unread email filtering
   - Alternatives: IMAP (deprecated, less secure), Gmail MCP server (additional complexity)

2. **LinkedIn Posting Method**
   - Decision: Use Playwright for browser automation (not LinkedIn API)
   - Rationale: LinkedIn API requires business verification, limited posting capabilities; Playwright provides full control
   - Alternatives: LinkedIn API (business verification required), third-party services (cost, security concerns)

3. **Priority Classification Logic**
   - Decision: Keyword-based rules + VIP sender list (configurable)
   - Rationale: Simple, transparent, easily adjustable; ML overkill for Phase 2
   - Alternatives: ML classifier (complex, training data needed), manual only (defeats automation)

4. **HITL Enforcement Mechanism**
   - Decision: Folder-based gate (only publish from /Approved)
   - Rationale: Leverages Phase 1 HITL workflow, no additional infrastructure
   - Alternatives: Metadata flag (easier to bypass), external approval system (complexity)

5. **Credential Management**
   - Decision: Reuse credentials.json from Phase 1, store in vault root
   - Rationale: Consistent with Phase 1, gitignored for security
   - Alternatives: Environment variables only (hard to manage multiple tokens), OS keychain (platform-specific)

**All NEEDS CLARIFICATION markers resolved. Proceeding to Phase 1 design.**

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](data-model.md) for complete entity definitions:
- EmailAlert (sender, subject, received_timestamp, priority, message_id, processed)
- SocialMediaPost (platform, content, media_path, scheduled_time, status, hitl_approved)
- CommunicationTriage (keywords, vip_senders, priority_rules)
- HITLGate (approval_path, rejection_path, feedback)

### API Contracts

See [contracts/](contracts/) for schema definitions:
- email-alert-schema.yaml - YAML frontmatter for email alerts
- social-media-post-schema.yaml - YAML frontmatter for LinkedIn posts

### Quickstart Guide

See [quickstart.md](quickstart.md) for setup and usage instructions.

### Agent Context Update

Gmail watcher and LinkedIn publisher patterns documented for Phase 2+ agents.

## Constitution Re-Check (Post-Design)

All principles remain satisfied after detailed design:

| Principle | Status | Verification |
|-----------|--------|--------------|
| I. Inbox-First | ✅ | Gmail watcher creates alerts in /Needs_Action |
| II. Schema Compliance | ✅ | Email alerts and posts have required frontmatter fields |
| III. Claim-By-Move | ✅ | LinkedIn agent claims posts via folder move |
| IV. HITL | ✅ | LinkedIn publisher only checks /Approved folder |
| V. Phase Lock | ✅ | Phase 1 Foundation is prerequisite (credentials.json exists) |
| VI. Audit Logging | ✅ | All Gmail/LinkedIn actions logged |
| VII. Minimalist | ✅ | Post generator enforces design rules |

**GATE RESULT**: ✅ PASS - Design verified against Constitution.

## Next Steps

Proceed to `/sp.tasks` to break this plan into implementation tasks.
