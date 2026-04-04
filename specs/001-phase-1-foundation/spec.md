# Feature Specification: Phase 1 Foundation - Digital FTE Nerve Center

**Feature Branch**: `001-phase-1-foundation`
**Created**: 2026-03-28
**Status**: Draft
**Input**: Establish the Digital FTE nerve center and local sensing capability

## User Scenarios & Testing

### User Story 1 - Dashboard Overview (Priority: P1)

As a business owner, I want to see a real-time overview of my business status (bank balance, pending messages, active projects) on a single dashboard so that I can quickly assess the current state of operations without checking multiple systems.

**Why this priority**: This is the primary interface for human-AI interaction. Without a clear dashboard, users cannot trust or effectively monitor the autonomous employee.

**Independent Test**: Can be fully tested by opening Dashboard.md and verifying all three sections (Bank Balance, Pending Messages, Active Projects) display accurate, formatted information.

**Acceptance Scenarios**:

1. **Given** the dashboard exists, **When** I open Dashboard.md, **Then** I see Bank Balance section with current balance and last transaction date
2. **Given** there are pending messages, **When** I view the dashboard, **Then** I see count and summary of unread emails and WhatsApp messages
3. **Given** there are active projects, **When** I view the dashboard, **Then** I see project names, status, and next action for each

---

### User Story 2 - Company Handbook (Priority: P1)

As the business owner, I want a Company Handbook that defines the "Rules of Engagement" for the AI employee so that the AI understands how to prioritize tasks, when to escalate, and what communication style to use.

**Why this priority**: The handbook is the foundational document that governs AI behavior. Without it, the AI cannot make consistent decisions aligned with business values.

**Independent Test**: Can be fully tested by opening Company_Handbook.md and verifying it contains Rules of Engagement section with clear, actionable guidelines.

**Acceptance Scenarios**:

1. **Given** the handbook exists, **When** I open Company_Handbook.md, **Then** I see Rules of Engagement section with priority rules
2. **Given** the handbook is complete, **When** I review it, **Then** I see escalation criteria for sensitive decisions
3. **Given** the handbook is referenced, **When** an AI agent processes a task, **Then** it follows the documented engagement rules

---

### User Story 3 - FileSystem Watcher Automation (Priority: P2)

As a user, I want to drop files into an /Inbox folder and have them automatically processed into metadata-rich task files in /Needs_Action so that I don't have to manually categorize and tag incoming items.

**Why this priority**: Automation of file intake is essential for scaling. Manual processing defeats the purpose of an autonomous employee.

**Independent Test**: Can be fully tested by dropping a test file into /Inbox and verifying a corresponding .md file appears in /Needs_Action with correct metadata.

**Acceptance Scenarios**:

1. **Given** a file is dropped in /Inbox, **When** the Watcher is running, **Then** a new .md file is created in /Needs_Action within 60 seconds
2. **Given** the file has a unique name, **When** processed, **Then** the metadata includes the original filename
3. **Given** a file with duplicate name exists, **When** processed, **Then** the system appends a timestamp to prevent overwriting
4. **Given** a file is processed, **When** I check the metadata, **Then** I see type, original_name, received_timestamp, and status fields populated

---

### User Story 4 - Audit Logging (Priority: P2)

As a compliance-conscious business owner, I want all system actions logged in daily JSON files so that I can audit what the AI employee did, when, and why.

**Why this priority**: Audit trails are critical for trust, compliance, and debugging. Without logs, there's no accountability.

**Independent Test**: Can be fully tested by performing actions and verifying entries appear in /Logs/YYYY-MM-DD.json with correct timestamps and action details.

**Acceptance Scenarios**:

1. **Given** the system is operational, **When** an action occurs, **Then** an entry is added to today's log file
2. **Given** it's a new day, **When** the first action occurs, **Then** a new log file is created with YYYY-MM-DD.json naming
3. **Given** an action is logged, **When** I review the entry, **Then** I see timestamp, action_type, agent_id, file_path, and status

---

### Edge Cases

- What happens when two files with identical names are dropped simultaneously? → System appends timestamp to metadata original_name field
- How does the system handle very large files (>100MB)? → Watcher logs warning, skips processing, moves to /Inbox/large_files/
- What happens when /Needs_Action is inaccessible (permissions issue)? → Watcher logs error to audit, pauses, retries every 5 minutes
- How does the system handle corrupted or unreadable files? → Watcher marks status as "error", includes error_message in metadata

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide a Dashboard.md file with three sections: Bank Balance, Pending Messages, and Active Projects
- **FR-002**: Dashboard MUST display current bank balance in USD with last updated timestamp
- **FR-003**: Dashboard MUST show count of pending messages from Gmail and WhatsApp separately
- **FR-004**: Dashboard MUST list active projects with name, status, and next action for each
- **FR-005**: System MUST provide a Company_Handbook.md file with Rules of Engagement section
- **FR-006**: Handbook MUST define task priority rules (urgent vs normal vs low)
- **FR-007**: Handbook MUST define escalation criteria for sensitive actions (payments, public communications)
- **FR-008**: System MUST include a Python-based FileSystem Watcher that monitors /Inbox directory
- **FR-009**: Watcher MUST detect new files within 60 seconds of creation
- **FR-010**: Watcher MUST create corresponding .md files in /Needs_Action with YAML frontmatter
- **FR-011**: Watcher MUST handle duplicate filenames by appending timestamp to prevent data loss
- **FR-012**: Metadata in /Needs_Action MUST include: type, original_name, received_timestamp, and status fields
- **FR-013**: System MUST create daily audit log files at /Logs/YYYY-MM-DD.json
- **FR-014**: Audit logs MUST record timestamp, action_type, agent_id, file_path, and status for each action
- **FR-015**: Audit logs MUST use JSON format with one entry per action

### Key Entities

- **Dashboard**: Central overview document displaying business status across three dimensions (financial, communications, projects)
- **Company Handbook**: Governance document defining AI behavior rules, priorities, and escalation procedures
- **FileSystem Watcher**: Background process monitoring /Inbox for new files and creating task metadata
- **Audit Log**: Daily JSON file recording all system actions for compliance and debugging
- **Task Metadata**: YAML frontmatter in /Needs_Action files containing type, original_name, received_timestamp, status

## Success Criteria

- **SC-001**: Users can view complete business overview (bank, messages, projects) in under 10 seconds by opening Dashboard.md
- **SC-002**: Dashboard accurately reflects current state with data less than 5 minutes old
- **SC-003**: FileSystem Watcher processes 100% of files dropped in /Inbox within 60 seconds
- **SC-004**: Zero data loss from duplicate filename collisions (all files processed with unique identifiers)
- **SC-005**: 100% of system actions are logged with complete metadata (timestamp, action, agent, file, status)
- **SC-006**: Users can retrieve any action from the past 30 days via audit log search in under 30 seconds
- **SC-007**: Company Handbook provides clear guidance for 95% of common scenarios without requiring human clarification

## Assumptions

- User has Python 3.11+ installed on local machine
- User has Obsidian or compatible Markdown editor for viewing dashboard and handbook
- /Inbox, /Needs_Action, /Logs directories exist per Constitution folder structure
- Bank balance data will be manually entered or integrated in later phases (Phase 2+)
- Gmail/WhatsApp integration for Pending Messages will be implemented in Phase 2 (Silver)
- Active Projects data will be derived from /In_Progress folder contents
