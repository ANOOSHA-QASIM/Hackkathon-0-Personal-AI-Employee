# Tasks: Phase 2 Functional - External Communication Senses

**Input**: Design documents from `/specs/002-phase-2-functional/`
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

- [X] T001 Create src/ directory structure: src/gmail/, src/linkedin/, src/triage/
- [X] T002 Create tests/ directory structure: tests/contract/, tests/integration/, tests/unit/
- [X] T003 [P] Create __init__.py files in all src/ subdirectories
- [ ] T004 Install Python dependencies: google-auth-oauthlib, google-api-python-client, playwright (pip install)
- [ ] T005 [P] Run `playwright install chromium` to install browser for LinkedIn automation
- [X] T006 [P] Create config/triage_rules.yaml with priority keywords and VIP sender list

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 [P] Extend src/config/settings.py with Gmail/LinkedIn configuration paths
- [X] T008 [P] Create src/gmail/gmail_auth.py with Gmail OAuth2 authentication function
- [X] T009 [P] Create Logs/processed_emails.json for email deduplication tracking
- [X] T010 Create credentials.json setup script (Gmail API OAuth2 flow)
- [X] T011 [P] Extend audit logger (src/audit/logger.py) with Gmail/LinkedIn action types
- [ ] T012 Test Gmail API connectivity (run gmail_auth.py --test)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Gmail Email Alerts (Priority: P1) 🎯 MVP

**Goal**: Implement Gmail watcher that monitors unread emails and creates .md alerts in /Needs_Action

**Independent Test**: Can be fully tested by sending a test email and verifying .md alert appears in /Needs_Action within 5 minutes with correct metadata (sender, subject, priority)

### Implementation for User Story 1

- [X] T013 [P] [US1] Create src/gmail/gmail_watcher.py with Gmail API connection
- [X] T014 [P] [US1] Implement check_unread_emails() function (query Gmail every 5 minutes)
- [X] T015 [US1] Create src/gmail/email_processor.py with parse_email() function
- [X] T016 [US1] Implement create_email_alert() function (write .md to /Needs_Action)
- [X] T017 [US1] Add email metadata extraction (sender, subject, received_timestamp, message_id)
- [X] T018 [US1] Implement is_email_processed() check (prevent duplicates via processed_emails.json)
- [X] T019 [US1] Add audit logging for all Gmail actions (email checked, alert created, duplicate skipped)
- [X] T020 [US1] Create src/gmail/__main__.py entry point (python -m gmail)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - LinkedIn Post Workflow with HITL (Priority: P1)

**Goal**: Implement LinkedIn posting with HITL approval (draft in /In_Progress, approve in /Approved, publish via Playwright)

**Independent Test**: Can be fully tested by creating draft post, moving to /Approved, and verifying post appears on LinkedIn within 10 minutes

### Implementation for User Story 2

- [X] T021 [P] [US2] Create src/linkedin/post_generator.py with create_draft_post() function
- [X] T022 [P] [US2] Implement generate_post_metadata() (platform, content, created_at, hitl_approved: false)
- [X] T023 [US2] Create LinkedIn post template in /Briefings/LinkedIn_Post_Template.md
- [X] T024 [US2] Create src/linkedin/linkedin_publisher.py with Playwright browser automation
- [X] T025 [US2] Implement login_to_linkedin() function (headless: false, headed mode)
- [X] T026 [US2] Implement check_approved_posts() function (monitor /Approved folder)
- [X] T027 [US2] Implement publish_post(metadata) function (post text + optional image)
- [X] T028 [US2] Add HITL gate enforcement (only publish if hitl_approved: true)
- [X] T029 [US2] Implement minimalist design validation for images (dark theme, clean typography)
- [X] T030 [US2] Add post-completion workflow (move to /Done, update status: published)
- [X] T031 [US2] Create src/linkedin/__main__.py entry point (python -m linkedin)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Communication Triage by Priority (Priority: P2)

**Goal**: Implement priority classification for emails/messages (High/Low based on keywords and VIP senders)

**Independent Test**: Can be fully tested by sending emails with different keywords and verifying priority tags in /Needs_Action alerts match expected categorization

### Implementation for User Story 3

- [X] T032 [P] [US3] Create src/triage/communication_triage.py with classify_priority() function
- [X] T033 [P] [US3] Implement load_triage_rules() function (read config/triage_rules.yaml)
- [X] T034 [US3] Implement check_vip_sender() function (VIP list lookup)
- [X] T035 [US3] Implement check_priority_keywords() function (subject line matching)
- [X] T036 [US3] Add keyword configuration (high: urgent, invoice, payment; low: newsletter, notification)
- [X] T037 [US3] Integrate triage with Gmail watcher (email_processor.py calls classify_priority())
- [X] T038 [US3] Add priority tags to email alert metadata (priority: high/normal/low)
- [X] T039 [US3] Create triage configuration UI (edit config/triage_rules.yaml instructions)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Social Media Metadata Schema (Priority: P2)

**Goal**: Implement structured metadata for social media posts (platform, content, media_path, scheduled_time, status)

**Independent Test**: Can be fully tested by creating a draft post and verifying YAML frontmatter includes all required metadata fields with correct values

### Implementation for User Story 4

- [X] T040 [P] [US4] Create src/linkedin/post_scheduler.py with check_scheduled_posts() function
- [X] T041 [P] [US4] Implement validate_post_metadata() function (check required fields)
- [X] T042 [US4] Add scheduled_time support (publish at exact time, within 2-minute window)
- [X] T043 [US4] Implement media_path validation (file exists, follows minimalist design)
- [X] T044 [US4] Add status tracking (draft → approved → published, or scheduled → published)
- [X] T045 [US4] Implement hitl_approved workflow (set hitl_approved: true when moved to /Approved)
- [X] T046 [US4] Add hitl_approved_by and hitl_approved_at fields on approval
- [X] T047 [US4] Create post revision workflow (move from /Approved back to /In_Progress for edits)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T048 [P] Create README.md section for Phase 2 (Gmail setup, LinkedIn workflow)
- [X] T049 [P] Update .gitignore to include Logs/processed_emails.json (contains email IDs)
- [X] T050 Add docstrings to all Gmail/LinkedIn/triage modules
- [X] T051 [P] Create run_gmail_watcher.bat batch file for Windows
- [X] T052 [P] Create run_linkedin_publisher.bat batch file for Windows
- [X] T053 Test full Gmail flow: send email → alert appears in /Needs_Action
- [ ] T054 Test full LinkedIn flow: create draft → approve → publish to LinkedIn
- [X] T055 Test triage accuracy: send emails with different keywords, verify priority tags
- [X] T056 Validate all email alerts have correct YAML frontmatter
- [ ] T057 Validate all LinkedIn posts have HITL approval before publishing
- [X] T058 Update Dashboard.md with Social & Email Feed section
- [X] T059 Run quickstart.md validation (follow all steps, verify no gaps)
- [X] T060 [P] Fix JSONDecodeError in load_processed_emails() (handle empty/invalid JSON)
- [X] T061 [P] Fix TypeError in log_action() (add **kwargs support)
- [X] T062 [P] Verify Gmail API userId='me' in all calls
- [X] T063 [P] Add check for missing processed_emails.json file
- [X] T064 [P] Ensure all paths are absolute (VAULT_ROOT)
- [X] T065 [P] Create src/agent/auto_drafter.py (watches /Needs_Action, generates drafts)
- [X] T066 [P] Update linkedin_poster.py with persistent browser context
- [X] T067 [P] Create src/gmail/gmail_sender.py (watches /Approved/Gmail, sends replies)
- [X] T068 [P] Migrate auto_drafter.py to Groq API (Llama 3.3 70B)
- [X] T069 [P] Create run_agent.bat batch file
- [X] T070 [P] Add requests library to requirements.txt
- [X] T071 [P] Fix gmail_auth.py: Delete token.json to force browser auth
- [X] T072 [P] Fix SCOPES to gmail.modify and gmail.send
- [X] T073 [P] Update gmail_sender.py with SUCCESS message
- [X] T074 [P] Update linkedin_poster.py with 60s login pause
- [X] T075 [P] Ensure persistent context saves session permanently
- [X] T076 [P] Create login_assistant.py for manual LinkedIn login
- [X] T077 [P] Add status field check (case-insensitive) in linkedin_poster.py
- [X] T078 [P] Fix .md file filter in /Approved folder
- [X] T079 [P] Add detailed skip logging with exact reasons
- [X] T080 [P] Ensure headless=False for visible posting
- [X] T081 [P] Fix log_action to accept **kwargs in gmail_sender.py
- [X] T082 [P] Add smart folder logic (bypass metadata checks in /Approved)
- [X] T083 [P] Add robust LinkedIn selectors (wait for .share-box-feed-entry__trigger)
- [X] T084 [P] Set 60s timeout for slow internet (Karachi)
- [X] T085 [P] Add try-except-finally for guaranteed browser cleanup
- [X] T086 [P] Add auto-cleanup (move to /Done after successful post)
- [X] T087 [P] Add debug logs with exact error messages
- [X] T088 [P] Fix log_action in linkedin_poster.py with **kwargs
- [X] T089 [P] Update LinkedIn selector to 'text=Start a post'
- [X] T090 [P] Increase all timeouts to 90s for Karachi internet
- [X] T091 [P] Add Post button selector 'button.share-actions__post-action'
- [X] T092 [P] Add 3s delay after typing for Post button to become clickable
- [X] T093 [P] Add success confirmation (editor disappears)
- [X] T094 [P] Move file to /Done ONLY on successful post
- [X] T095 [P] SMART FOLDER: Location = approval (ignore YAML status/hitl_approved)
- [X] T096 [P] Process ANY .md file in /Approved folder (filename flexible)

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

- **User Story 1 (Gmail Alerts)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (LinkedIn HITL)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (Triage)**: Can start after Foundational (Phase 2) - Depends on US1 (Gmail watcher integration)
- **User Story 4 (Metadata)**: Can start after Foundational (Phase 2) - Depends on US2 (LinkedIn post workflow)

### Within Each User Story

- Models before services
- Services before endpoints/UI
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 (Setup)**: T003, T005, T006 can run in parallel
- **Phase 2 (Foundational)**: T007, T008, T009, T011 can run in parallel
- **Phase 3 (US1)**: T013, T014, T015 can run in parallel
- **Phase 4 (US2)**: T021, T022, T023 can run in parallel
- **Phase 5 (US3)**: T032, T033 can run in parallel
- **Phase 6 (US4)**: T040, T041 can run in parallel
- **Phase 7 (Polish)**: T048, T049, T051, T052 can run in parallel

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Gmail Alerts)
   - Developer B: User Story 2 (LinkedIn HITL)
   - Developer C: User Story 3 (Triage) - after US1 complete
   - Developer D: User Story 4 (Metadata) - after US2 complete
3. Stories complete and integrate independently

---

## Parallel Example: User Story 1 (Gmail Alerts)

```bash
# Launch all parallel tasks for User Story 1:
Task: "T013 [P] [US1] Create src/gmail/gmail_watcher.py with Gmail API connection"
Task: "T014 [P] [US1] Implement check_unread_emails() function (query Gmail every 5 minutes)"
Task: "T015 [US1] Create src/gmail/email_processor.py with parse_email() function"
```

---

## Parallel Example: Foundational Phase

```bash
# Launch all parallel tasks for Foundational:
Task: "T007 [P] Extend src/config/settings.py with Gmail/LinkedIn configuration paths"
Task: "T008 [P] Create src/gmail/gmail_auth.py with Gmail OAuth2 authentication function"
Task: "T009 [P] Create Logs/processed_emails.json for email deduplication tracking"
Task: "T011 [P] Extend audit logger with Gmail/LinkedIn action types"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T012)
3. Complete Phase 3: User Story 1 (T013-T020)
4. **STOP and VALIDATE**: Send test email → verify alert in /Needs_Action
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 (Gmail Alerts) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 (LinkedIn HITL) → Test independently → Deploy/Demo
4. Add User Story 3 (Triage) → Test independently → Deploy/Demo
5. Add User Story 4 (Metadata Schema) → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Full Phase 2 Delivery

1. Complete all phases (T001-T059)
2. Run integration tests (T053-T057)
3. Validate HITL enforcement (T057)
4. Mark Phase 2 as 'Closed' per Constitution Principle V
5. Ready for Phase 3 (Gold: Odoo Accounting, Business Audit)

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
| Phase 1 | Setup | 6 tasks |
| Phase 2 | Foundational | 6 tasks |
| Phase 3 | User Story 1 (Gmail Alerts) | 8 tasks |
| Phase 4 | User Story 2 (LinkedIn HITL) | 11 tasks |
| Phase 5 | User Story 3 (Triage) | 8 tasks |
| Phase 6 | User Story 4 (Metadata) | 8 tasks |
| Phase 7 | Polish | 12 tasks |
| **Total** | | **59 tasks** |

**MVP Scope**: Phases 1-3 (T001-T020) = 20 tasks → Gmail alerts ready for demo
