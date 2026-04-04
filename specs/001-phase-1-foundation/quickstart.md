# Quickstart: Phase 1 Foundation

**Feature**: 001-phase-1-foundation  
**Last Updated**: 2026-03-28  
**Status**: Draft

## Overview

Phase 1 Foundation establishes the Digital FTE nerve center with:
- **Dashboard.md**: Business status overview (bank, messages, projects)
- **Company_Handbook.md**: AI behavior rules and escalation criteria
- **FileSystem Watcher**: Automatic file intake from /Inbox to /Needs_Action
- **Audit Logging**: Daily JSON logs for compliance

## Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Obsidian (or any Markdown editor)
- Windows (E:/ drive local filesystem)

## Installation

### Step 1: Install Python Dependencies

```bash
cd E:\hackathon_0_digital_fte\AI_Employee_vault
pip install watchdog pyyaml python-dotenv
```

### Step 2: Create Required Directories

```bash
mkdir Inbox
mkdir Needs_Action
mkdir In_Progress
mkdir Approved
mkdir Rejected
mkdir Done
mkdir Logs
mkdir Accounting
mkdir Briefings
```

### Step 3: Verify Folder Structure

Your vault should now have this structure:

```
E:/hackathon_0_digital_fte/AI_Employee_vault/
├── Inbox/              # Drop files here
├── Needs_Action/       # Auto-created tasks
├── In_Progress/        # Claimed tasks
├── Approved/           # HITL-approved tasks
├── Rejected/           # Rejected tasks
├── Done/               # Completed tasks
├── Logs/               # Audit logs
├── Dashboard.md        # Business overview
└── Company_Handbook.md # AI rules
```

## Usage

### FileSystem Watcher

#### Start the Watcher

```bash
python src/watcher/file_watcher.py
```

The watcher will:
1. Monitor `/Inbox` for new files
2. Detect files within 60 seconds
3. Create corresponding `.md` files in `/Needs_Action` with metadata
4. Log all actions to `/Logs/YYYY-MM-DD.json`

#### Test the Watcher

1. Drop a test file into `/Inbox`:
   ```bash
   echo "Test content" > "Inbox/test-document.txt"
   ```

2. Wait up to 60 seconds

3. Verify the task file was created in `/Needs_Action`:
   ```bash
   dir Needs_Action\*.md
   ```

4. Check the metadata:
   ```markdown
   ---
   status: Needs_Action
   type: file_drop
   original_name: test-document.txt
   received_timestamp: 2026-03-28T10:30:00Z
   tags:
     - test
   ---
   
   ## Task Description
   
   Process this test file.
   ```

5. Check the audit log:
   ```bash
   type Logs\2026-03-28.json
   ```

### Dashboard

#### Open Dashboard.md

1. Open `Dashboard.md` in Obsidian
2. Review the three sections:
   - **Bank Balance**: Current balance (manual entry)
   - **Pending Messages**: Unread count (manual entry)
   - **Active Projects**: Project status table (manual entry)

#### Update Dashboard (Manual - Phase 1)

Edit `Dashboard.md` directly:

```markdown
## Bank Balance

- **Current Balance**: $5,432.10 USD
- **Last Updated**: 2026-03-28 09:00 AM

## Pending Messages

- **Gmail**: 12 unread
- **WhatsApp**: 5 unread

## Active Projects

| Project | Status | Next Action |
|---------|--------|-------------|
| Website Redesign | In_Progress | Review mockups |
```

**Note**: Phase 2+ will automate dashboard updates from Gmail API, bank APIs, etc.

### Company Handbook

#### Open Company_Handbook.md

1. Open `Company_Handbook.md` in Obsidian
2. Review the Rules of Engagement

#### Add Custom Rules

Edit `Company_Handbook.md` to add your business-specific rules:

```markdown
### RULE-001: Payment Escalation

**Category**: Escalation

**Description**: All payments exceeding $500 USD MUST be moved to /Approved for human review before processing.

### RULE-002: Response Time

**Category**: Communication

**Description**: All email replies should be drafted within 4 hours during business hours (9 AM - 6 PM EST).
```

### Audit Logs

#### View Today's Log

```bash
type Logs\2026-03-28.json
```

#### Search Logs

Use `jq` (JSON processor) or any JSON viewer:

```bash
# Install jq first: https://stedolan.github.io/jq/download/

# Count actions by type
jq '[.entries[].action_type] | group_by(.) | map({type: .[0], count: length})' Logs\2026-03-28.json

# Find errors
jq '.entries[] | select(.status == "error")' Logs\2026-03-28.json
```

## Troubleshooting

### Watcher Not Detecting Files

1. **Check watcher is running**:
   ```bash
   tasklist | findstr python
   ```

2. **Verify /Inbox path**:
   ```bash
   dir Inbox
   ```

3. **Check permissions**:
   - Ensure watcher has read access to `/Inbox`
   - Ensure watcher has write access to `/Needs_Action` and `/Logs`

4. **Review watcher logs**:
   ```bash
   type Logs\2026-03-28.json | findstr error
   ```

### Metadata File Not Created

1. **Check disk space**:
   ```bash
   wmic logicaldisk where "DeviceID='E:'" get FreeSpace
   ```

2. **Verify YAML dependency**:
   ```bash
   pip show pyyaml
   ```

3. **Check for duplicate handling**:
   - Files with same name get timestamp-prefixed filenames
   - Check `/Needs_Action` for `YYYYMMDD_HHMMSS_*.md` pattern

### Audit Log Errors

1. **Check log file permissions**:
   - Ensure `/Logs` directory is writable

2. **Verify JSON schema**:
   - Logs must match schema in `contracts/audit-log-schema.json`

3. **Check for concurrent writes**:
   - Only one watcher should write to the same log file
   - Phase 2+ will implement file locking

## Next Steps

### Phase 1 Completion Checklist

- [ ] Watcher detects files within 60 seconds
- [ ] Metadata includes all required fields (status, type, original_name, timestamp)
- [ ] Duplicate filenames handled correctly
- [ ] Dashboard.md created with all three sections
- [ ] Company_Handbook.md created with Rules of Engagement
- [ ] Audit logs created in `/Logs/YYYY-MM-DD.json`
- [ ] All actions logged with correct schema

### Phase 2 Preparation

Once Phase 1 is complete, you're ready for:
- Gmail Watcher (automated email detection)
- WhatsApp Watcher (automated message detection)
- HITL approval workflow
- Dashboard automation (API integrations)

## Support

For issues or questions:
1. Check audit logs: `/Logs/YYYY-MM-DD.json`
2. Review Constitution: `.specify/memory/constitution.md`
3. Consult data model: `specs/001-phase-1-foundation/data-model.md`
