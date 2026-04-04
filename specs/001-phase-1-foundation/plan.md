# Implementation Plan: Phase 1 Foundation

**Branch**: `001-phase-1-foundation` | **Date**: 2026-03-28 | **Spec**: [specs/001-phase-1-foundation/spec.md](../spec.md)

**Input**: Design the technical roadmap for the Digital FTE Foundation Layer with Dashboard, Handbook, FileSystem Watcher, and Audit Logging.

## Summary

Build the foundational layer for the Digital FTE autonomous employee system. The system provides a business dashboard for real-time status overview, a company handbook defining AI behavior rules, a Python-based FileSystem Watcher for automatic file intake processing, and daily audit logging for compliance. All components follow the Constitution's folder structure and claim-by-move protocol.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: watchdog (file monitoring), pyyaml (YAML parsing), python-dotenv (environment config)
**Storage**: File-based (Markdown files with YAML frontmatter, JSON audit logs)
**Testing**: pytest for unit tests, integration tests for watcher functionality
**Target Platform**: Windows (E:/ drive local filesystem)
**Project Type**: Single Python service with file-based state management
**Performance Goals**: 
- Watcher detects files within 60 seconds
- Dashboard loads in under 10 seconds
- Zero data loss on duplicate filenames
**Constraints**: 
- Must use Constitution-defined folder structure
- All actions logged to /Logs/YYYY-MM-DD.json
- No external API calls in Phase 1 (manual data entry)
**Scale/Scope**: 
- Single user (business owner)
- Local filesystem only
- <100 files/day processing volume expected

## Constitution Check

**GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.**

| Principle | Compliance | Notes |
|-----------|------------|-------|
| I. Inbox-First Data Entry | ✅ PASS | Watcher monitors /Inbox, moves to /Needs_Action with metadata |
| II. Needs_Action Schema Compliance | ✅ PASS | All task files include YAML frontmatter with required fields |
| III. Claim-By-Move Protocol | ✅ PASS | Dashboard reads /In_Progress for active projects; agents claim via move |
| IV. HITL Mandatory for External Actions | ✅ PASS | Phase 1 has no external actions; handbook defines escalation for future |
| V. Strict Phase Lock | ✅ PASS | This is Phase 1; no Phase 2+ features included |
| VI. Audit Logging | ✅ PASS | All watcher actions logged to /Logs/YYYY-MM-DD.json |
| VII. Minimalist Design | ✅ PASS | Dashboard uses plain Markdown, no images/icons |

**GATE RESULT**: ✅ PASS - All principles satisfied. Proceed to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/001-phase-1-foundation/
├── plan.md              # This file
├── research.md          # Phase 0 output (technical research)
├── data-model.md        # Phase 1 output (entity definitions)
├── quickstart.md        # Phase 1 output (setup guide)
└── contracts/           # Phase 1 output (schemas)
    └── audit-log-schema.json
```

### Source Code (repository root)

```text
src/
├── watcher/
│   ├── __init__.py
│   ├── base_watcher.py    # BaseWatcher pattern implementation
│   ├── file_watcher.py    # FileSystem Watcher for /Inbox
│   └── metadata.py        # YAML frontmatter generation
├── dashboard/
│   ├── __init__.py
│   └── generator.py       # Dashboard.md generation logic
├── audit/
│   ├── __init__.py
│   └── logger.py          # Audit log writing and sealing
└── config/
    ├── __init__.py
    └── settings.py        # Environment configuration

tests/
├── contract/
│   └── test_audit_schema.py
├── integration/
│   └── test_watcher_flow.py
└── unit/
    ├── test_base_watcher.py
    ├── test_metadata.py
    └── test_audit_logger.py
```

**Structure Decision**: Single Python project structure with modular design. Watcher, dashboard, and audit components are separate modules for future extensibility (Phase 2+ watchers will inherit from BaseWatcher).

## Complexity Tracking

No violations. All design decisions align with Constitution principles.

## Phase 0: Research & Technical Decisions

### Research Tasks Completed

1. **File System Monitoring Pattern**
   - Decision: Use `watchdog` library for cross-platform file monitoring
   - Rationale: Industry standard, efficient (uses OS-level APIs), supports debouncing
   - Alternatives: Polling (inefficient), Windows API directly (not portable)

2. **YAML Frontmatter Format**
   - Decision: Use `pyyaml` for parsing/generating YAML frontmatter
   - Rationale: Standard library, handles edge cases, well-maintained
   - Alternatives: Manual string parsing (error-prone), ruamel.yaml (overkill for simple frontmatter)

3. **Audit Log Schema Design**
   - Decision: JSON Schema with required fields (timestamp, action_type, agent_id, file_path, status)
   - Rationale: Machine-readable, extensible, supports future sealing with hash
   - Alternatives: CSV (not extensible), Markdown (harder to parse)

4. **Duplicate File Handling Strategy**
   - Decision: Append timestamp to metadata `original_name` field, not filename
   - Rationale: Preserves original filename for reference, prevents data loss
   - Alternatives: Overwrite (data loss), skip file (user confusion)

5. **Dashboard Update Strategy**
   - Decision: Manual update in Phase 1 (placeholder data), automated in Phase 2+
   - Rationale: External integrations (Gmail, bank APIs) are Phase 2+ features
   - Alternatives: Mock data only (misleading), delay dashboard (reduces early value)

**All NEEDS CLARIFICATION markers resolved. Proceeding to Phase 1 design.**

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](data-model.md) for complete entity definitions:
- TaskMetadata (YAML frontmatter schema)
- AuditLogEntry (JSON log entry schema)
- DashboardSection (Dashboard.md structure)
- HandbookRule (Company_Handbook.md structure)

### API Contracts

See [contracts/audit-log-schema.json](contracts/audit-log-schema.json) for JSON Schema definition.

### Quickstart Guide

See [quickstart.md](quickstart.md) for setup and usage instructions.

### Agent Context Update

BaseWatcher pattern documented for future watcher implementations (Phase 2+).

## Constitution Re-Check (Post-Design)

All principles remain satisfied after detailed design:

| Principle | Status | Verification |
|-----------|--------|--------------|
| I. Inbox-First | ✅ | Watcher only monitors /Inbox |
| II. Schema Compliance | ✅ | metadata.py enforces required fields |
| III. Claim-By-Move | ✅ | Dashboard reads /In_Progress folder structure |
| IV. HITL | ✅ | No external actions in Phase 1 |
| V. Phase Lock | ✅ | Scope bounded to Phase 1 exit criteria |
| VI. Audit Logging | ✅ | All actions logged with full schema |
| VII. Minimalist | ✅ | Plain Markdown, no visual clutter |

**GATE RESULT**: ✅ PASS - Design verified against Constitution.

## Next Steps

Proceed to `/sp.tasks` to break this plan into implementation tasks.
