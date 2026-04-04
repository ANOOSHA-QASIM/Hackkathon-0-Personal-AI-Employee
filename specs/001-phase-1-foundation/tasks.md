# Tasks: Phase 1 Foundation - Digital FTE Nerve Center

**Input**: Design documents from `/specs/001-phase-1-foundation/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - not explicitly requested in spec. Implementation tasks only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- All paths relative to `E:/hackathon_0_digital_fte/AI_Employee_vault/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create src/ directory structure: src/watcher/, src/dashboard/, src/audit/, src/config/
- [X] T002 Create tests/ directory structure: tests/contract/, tests/integration/, tests/unit/
- [X] T003 [P] Create __init__.py files in all src/ subdirectories
- [ ] T004 Install Python dependencies: watchdog, pyyaml, python-dotenv (pip install)
- [X] T005 [P] Create .env.example with VAULT_ROOT=E:/hackathon_0_digital_fte/AI_Employee_vault

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 [P] Create src/config/settings.py with environment variable loading
- [X] T007 [P] Create src/audit/logger.py with AuditLogger class (write_audit_entry function)
- [X] T008 [P] Create src/watcher/metadata.py with YAML frontmatter generation functions
- [X] T009 Create src/watcher/base_watcher.py with BaseWatcher abstract base class
- [ ] T010 [P] Create contracts/audit-log-schema.json validation test in tests/contract/test_audit_schema.py
- [X] T011 Create vault root directories: Inbox/, Needs_Action/, In_Progress/, Approved/, Rejected/, Done/, Logs/, Accounting/, Briefings/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Dashboard Overview (Priority: P1) 🎯 MVP

**Goal**: Create Dashboard.md with three sections (Bank Balance, Pending Messages, Active Projects) for business status overview

**Independent Test**: Can be fully tested by opening Dashboard.md and verifying all three sections display accurate, formatted information

### Implementation for User Story 1

- [X] T012 [P] [US1] Create Dashboard.md in vault root with ## Bank Balance section (manual entry fields)
- [X] T013 [P] [US1] Add ## Pending Messages section to Dashboard.md (Gmail/WhatsApp counts)
- [X] T014 [US1] Add ## Active Projects section to Dashboard.md (table with Status, Next Action columns)
- [X] T015 [US1] Add Quick Links section to Dashboard.md with links to Handbook, Inbox, Needs_Action
- [X] T016 [US1] Create src/dashboard/generator.py with DashboardGenerator class (read/write dashboard sections)
- [X] T017 [US1] Add update_dashboard() function in src/dashboard/generator.py for manual data entry

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Company Handbook (Priority: P1)

**Goal**: Create Company_Handbook.md with Rules of Engagement for AI behavior governance

**Independent Test**: Can be fully tested by opening Company_Handbook.md and verifying it contains Rules of Engagement section with priority rules and escalation criteria

### Implementation for User Story 2

- [X] T018 [P] [US2] Create Company_Handbook.md in vault root with Purpose section
- [X] T019 [P] [US2] Add Priority Rules section (RULE-001: Task Prioritization, RULE-002: FIFO)
- [X] T020 [US2] Add Escalation Rules section (RULE-003: Payment Escalation, RULE-004: Communication Escalation)
- [X] T021 [US2] Add Workflow Rules section (RULE-008: Claim-by-Move, RULE-009: Audit Logging)
- [X] T022 [US2] Add Security Rules section (RULE-011: Credential Handling, RULE-012: Data Protection)
- [X] T023 [US2] Add Decision Matrix and Quick Reference table to Company_Handbook.md

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - FileSystem Watcher Automation (Priority: P2)

**Goal**: Implement Python FileSystem Watcher that monitors /Inbox and creates metadata-rich .md files in /Needs_Action

**Independent Test**: Can be fully tested by dropping a test file into /Inbox and verifying a corresponding .md file appears in /Needs_Action with correct metadata

### Implementation for User Story 3

- [X] T024 [P] [US3] Create src/watcher/file_watcher.py with FileSystemWatcher class (inherits BaseWatcher)
- [X] T025 [P] [US3] Implement check() method in FileSystemWatcher (watchdog Observer for /Inbox monitoring)
- [X] T026 [US3] Implement transform_event() method in FileSystemWatcher (file event → task metadata)
- [X] T027 [US3] Implement duplicate handling in file_watcher.py (timestamp-prefixed filenames)
- [X] T027b [US3] Add 0.5s delay before processing (wait for OS file write completion)
- [X] T028 [US3] Add large file detection (>100MB) with warning log and skip logic
- [X] T028b [US3] Add try-except for shutil.move (catch PermissionError on Windows)
- [X] T028c [US3] Ensure file is MOVED (not copied) from Inbox to Needs_Action
- [X] T029 [US3] Create src/watcher/__main__.py with watcher entry point (python -m watcher)
- [X] T029b [US3] Create standalone base_watcher.py in vault root (direct execution, no imports)
- [ ] T030 [US3] Add integration test in tests/integration/test_watcher_flow.py (drop file → verify metadata)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Audit Logging (Priority: P2)

**Goal**: Ensure all system actions are logged to /Logs/YYYY-MM-DD.json with complete metadata

**Independent Test**: Can be fully tested by performing actions and verifying entries appear in /Logs/YYYY-MM-DD.json with correct timestamps and action details

### Implementation for User Story 4

- [X] T031 [P] [US4] Create initial /Logs/2026-03-28.json with system_init event entry
- [X] T032 [P] [US4] Implement log_action() in src/audit/logger.py (append to daily log)
- [ ] T033 [US4] Add JSON schema validation in src/audit/logger.py (validate against audit-log-schema.json)
- [X] T034 [US4] Implement daily log rotation (create new file on new day)
- [X] T035 [US4] Add seal_audit_log() function in src/audit/logger.py (SHA-256 hash at EOD)
- [X] T036 [US4] Integrate audit logging into BaseWatcher (all actions logged automatically)
- [ ] T037 [US4] Add error handling for log write failures (retry, then alert)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T038 [P] Create README.md with Phase 1 setup instructions (link to quickstart.md)
- [X] T039 [P] Create .gitignore with __pycache__/, *.pyc, .env, Logs/
- [ ] T040 Add docstrings to all Python modules
- [X] T041 [P] Create run_watcher.bat batch file for Windows (python -m watcher)
- [ ] T042 Test full flow: drop file → watcher detects → metadata created → audit logged
- [ ] T043 Validate Dashboard.md renders correctly in Obsidian Edit and Reading modes
- [ ] T044 Validate Company_Handbook.md contains all 12 rules with clear boundaries
- [ ] T045 Run quickstart.md validation (follow all steps, verify no gaps)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order: US1 → US2 → US3 → US4
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (Dashboard)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (Handbook)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (Watcher)**: Can start after Foundational (Phase 2) - Uses BaseWatcher from Phase 2
- **User Story 4 (Audit)**: Can start after Foundational (Phase 2) - Uses AuditLogger from Phase 2

### Within Each User Story

- Models before services
- Services before endpoints/UI
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 (Setup)**: T003, T005 can run in parallel
- **Phase 2 (Foundational)**: T006, T007, T008 can run in parallel
- **Phase 3 (US1)**: T012, T013 can run in parallel
- **Phase 4 (US2)**: T018, T019 can run in parallel
- **Phase 5 (US3)**: T024, T025 can run in parallel
- **Phase 6 (US4)**: T031, T032 can run in parallel
- **Phase 7 (Polish)**: T038, T039, T041 can run in parallel

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Dashboard)
   - Developer B: User Story 2 (Handbook)
   - Developer C: User Story 3 (Watcher)
   - Developer D: User Story 4 (Audit)
3. Stories complete and integrate independently

---

## Parallel Example: User Story 1 (Dashboard)

```bash
# Launch all parallel tasks for User Story 1:
Task: "T012 [P] [US1] Create Dashboard.md in vault root with ## Bank Balance section"
Task: "T013 [P] [US1] Add ## Pending Messages section to Dashboard.md"
```

---

## Parallel Example: Foundational Phase

```bash
# Launch all parallel tasks for Foundational:
Task: "T006 [P] Create src/config/settings.py with environment variable loading"
Task: "T007 [P] Create src/audit/logger.py with AuditLogger class"
Task: "T008 [P] Create src/watcher/metadata.py with YAML frontmatter generation"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T011)
3. Complete Phase 3: User Story 1 (T012-T017)
4. **STOP and VALIDATE**: Open Dashboard.md, verify all three sections
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Dashboard) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (Handbook) → Test independently → Deploy/Demo
4. Add User Story 3 (Watcher) → Test independently → Deploy/Demo
5. Add User Story 4 (Audit) → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Full Phase 1 Delivery

1. Complete all phases (T001-T045)
2. Run integration test (T042): drop file → watcher → metadata → audit
3. Validate Obsidian rendering (T043, T044)
4. Mark Phase 1 as 'Closed' per Constitution Principle V
5. Ready for Phase 2 (Silver: Gmail/WhatsApp Watchers)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability (US1, US2, US3, US4)
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

| Phase | Description | Task Count |
|-------|-------------|------------|
| Phase 1 | Setup | 5 tasks |
| Phase 2 | Foundational | 6 tasks |
| Phase 3 | User Story 1 (Dashboard) | 6 tasks |
| Phase 4 | User Story 2 (Handbook) | 6 tasks |
| Phase 5 | User Story 3 (Watcher) | 7 tasks |
| Phase 6 | User Story 4 (Audit) | 7 tasks |
| Phase 7 | Polish | 8 tasks |
| **Total** | | **45 tasks** |

**MVP Scope**: Phases 1-3 (T001-T017) = 17 tasks → Dashboard ready for demo
