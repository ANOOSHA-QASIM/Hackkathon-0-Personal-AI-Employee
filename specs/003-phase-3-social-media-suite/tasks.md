# Tasks: Phase 3 Social Media Suite

**Input**: Design documents from `/specs/003-phase-3-social-media-suite/`
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

- [X] T001 Create src/skills/ directory structure
- [X] T002 Create src/orchestrator/ directory structure
- [X] T003 Create src/utils/ directory structure
- [X] T004 [P] Create __init__.py files in all src/ subdirectories
- [X] T005 [P] Create .browser_data/ directory for persistent sessions
- [X] T006 [P] Create /Approved/Social/ folder for post approval workflow

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 [P] Create src/skills/base_poster.py with BasePoster abstract class
- [ ] T008 [P] Extend src/config/settings.py with social media configuration
- [ ] T009 [P] Create src/utils/ralph_wiggum.py with RalphWiggum error recovery class
- [X] T010 [P] Create src/social/login_helper.py for manual session setup
- [ ] T011 Test session setup (run login_helper.py for Meta and Twitter)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Cross-Platform Social Posting (Priority: P1) 🎯 MVP

**Goal**: Implement Cross-Platform Orchestrator that posts to all 4 platforms from single file

**Independent Test**: Can be fully tested by creating a post file in `/Approved/Social/` and verifying it publishes to all 4 platforms within 10 minutes

### Implementation for User Story 1

- [ ] T012 [P] [US1] Create src/orchestrator/social_dispatcher.py with SocialDispatcher class
- [ ] T013 [P] [US1] Implement watch_approved_social() function to detect new posts
- [ ] T014 [US1] Implement trigger_all_platforms() function to coordinate posting
- [ ] T015 [US1] Add platform sequencing logic (LinkedIn → Facebook → Instagram → Twitter)
- [ ] T016 [US1] Integrate LinkedIn poster (reuse Phase 2 src/linkedin/linkedin_poster.py)
- [ ] T017 [US1] Integrate Meta poster (call src/skills/meta_poster.py)
- [ ] T018 [US1] Integrate Twitter poster (call src/skills/twitter_poster.py)
- [ ] T019 [US1] Add per-platform status tracking in post metadata
- [ ] T020 [US1] Add success handling (move to /Done/Social/ when all platforms succeed)
- [ ] T021 [US1] Add partial failure handling (track which platforms failed)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Meta Platform Integration (Priority: P1)

**Goal**: Implement Meta Poster skill for Facebook and Instagram with persistent sessions

**Independent Test**: Can be fully tested by logging in once to Facebook/Instagram, then verifying subsequent posts publish without requiring re-authentication

### Implementation for User Story 2

- [X] T022 [P] [US2] Create src/skills/meta_poster.py with MetaPoster class
- [X] T023 [P] [US2] Implement _launch_browser() with persistent session (.browser_data/meta)
- [ ] T024 [US2] Implement authenticate() function for manual login (first time only)
- [ ] T025 [US2] Implement post_to_facebook() function (navigate, type caption, upload image, publish)
- [ ] T026 [US2] Implement post_to_instagram() function (navigate, type caption, upload image, publish)
- [ ] T027 [US2] Add image upload handling from media_path metadata
- [ ] T028 [US2] Add session expiration detection and re-authentication flow
- [ ] T029 [US2] Add content validation (Instagram 2200 char limit, Facebook 63206 char limit)
- [ ] T030 [US2] Add PostingResult return type with platform URL and timestamps
- [ ] T031 [US2] Create src/skills/__init__.py to export MetaPoster

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Twitter (X) Integration (Priority: P2)

**Goal**: Implement Twitter Poster skill with auto-threading for long content

**Independent Test**: Can be fully tested by creating a post with >280 characters and verifying it appears as a properly formatted thread on Twitter

### Implementation for User Story 3

- [X] T032 [P] [US3] Create src/skills/twitter_poster.py with TwitterPoster class
- [X] T033 [P] [US3] Implement _launch_browser() with persistent session (.browser_data/twitter)
- [ ] T034 [US3] Implement authenticate() function for manual login (first time only)
- [ ] T035 [US3] Implement _split_into_thread() function (280 char split with "..." separator)
- [ ] T036 [US3] Implement post_tweet_thread() function (post single tweet or thread)
- [ ] T037 [US3] Add image attachment to first tweet in thread
- [ ] T038 [US3] Add content validation (280 char limit per tweet)
- [ ] T039 [US3] Add PostingResult return type with tweet URL and timestamps
- [ ] T040 [US3] Create test for auto-threading (post >280 chars, verify thread)

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: User Story 4 - Ralph Wiggum Error Recovery (Priority: P2)

**Goal**: Implement autonomous error recovery with retry logic and escalation

**Independent Test**: Can be fully tested by simulating an API failure and verifying the post is retried and eventually published after the cooldown period

### Implementation for User Story 4

- [ ] T041 [P] [US4] Extend src/utils/ralph_wiggum.py with retry_on_failure() function
- [ ] T042 [P] [US4] Implement 15-minute cooldown between retries
- [ ] T043 [US4] Implement max 3 retry attempts logic
- [ ] T044 [US4] Add error logging to /Logs/YYYY-MM-DD.json with platform and error details
- [ ] T045 [US4] Implement escalation to /Needs_Action/ after 3 failed retries
- [ ] T046 [US4] Integrate Ralph Wiggum wrapper into social_dispatcher.py
- [ ] T047 [US4] Add per-platform retry tracking in platform_results metadata
- [ ] T048 [US4] Add next_retry_at timestamp for scheduled retries
- [ ] T049 [US4] Create test for Ralph Wiggum (simulate failure, verify retry + escalation)

**Checkpoint**: All user stories should now be independently functional with error recovery

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T050 [P] Create README.md section for Phase 3 (Meta/Twitter setup, session management)
- [ ] T051 [P] Update Company_Handbook.md with social media approval instructions
- [ ] T052 [P] Create run_social_dispatcher.bat batch file for Windows
- [ ] T053 Add docstrings to all Meta/Twitter/Ralph Wiggum modules
- [ ] T054 Test full Meta flow: login once → post multiple times without re-auth
- [ ] T055 Test full Twitter flow: post long content → verify auto-threading
- [ ] T056 Test full orchestrator flow: single file → all 4 platforms
- [ ] T057 Test Ralph Wiggum: simulate platform failure → verify retry + escalation
- [ ] T058 Validate all posts logged to /Logs/YYYY-MM-DD.json
- [ ] T059 Run quickstart.md validation (follow all steps, verify no gaps)
- [ ] T060 [P] Add verbose logging option to social_dispatcher.py (--verbose flag)
- [ ] T061 [P] Add platform-specific error messages (user-friendly)
- [ ] T062 [P] Create /Done/Social/ subfolder structure (archive by YYYY-MM)

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

- **User Story 1 (Cross-Platform)**: Can start after Foundational (Phase 2) - Depends on US2, US3 skills
- **User Story 2 (Meta)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (Twitter)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (Ralph Wiggum)**: Can start after US1 complete (needs orchestrator to wrap)

### Within Each User Story

- Models/base classes before services
- Services before orchestrator integration
- Core implementation before error handling
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 (Setup)**: T001-T006 can all run in parallel
- **Phase 2 (Foundational)**: T007-T010 can all run in parallel
- **Phase 3 (US1)**: T012-T013 can run in parallel, then T014-T021 sequential
- **Phase 4 (US2)**: T022-T023 can run in parallel, then T024-T031 sequential
- **Phase 5 (US3)**: T032-T033 can run in parallel, then T034-T040 sequential
- **Phase 6 (US4)**: T041-T042 can run in parallel, then T043-T049 sequential
- **Phase 7 (Polish)**: T050-T053 can run in parallel, T054-T059 sequential (tests)

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 2 (Meta Poster)
   - Developer B: User Story 3 (Twitter Poster)
   - Developer C: User Story 1 (Orchestrator) - waits for A+B
3. After US1, US2, US3 complete:
   - Developer A: User Story 4 (Ralph Wiggum)
   - Developer B: Phase 7 Polish (documentation, tests)
4. Stories complete and integrate independently

---

## Parallel Example: User Story 2 (Meta)

```bash
# Launch parallel setup tasks for User Story 2:
Task: "T022 [P] [US2] Create src/skills/meta_poster.py with MetaPoster class"
Task: "T023 [P] [US2] Implement _launch_browser() with persistent session"

# Then sequential implementation:
Task: "T024 [US2] Implement authenticate() function"
Task: "T025 [US2] Implement post_to_facebook() function"
Task: "T026 [US2] Implement post_to_instagram() function"
```

---

## Parallel Example: Foundational Phase

```bash
# Launch all parallel tasks for Foundational:
Task: "T007 [P] Create src/skills/base_poster.py with BasePoster abstract class"
Task: "T008 [P] Extend src/config/settings.py with social media configuration"
Task: "T009 [P] Create src/utils/ralph_wiggum.py with RalphWiggum error recovery class"
Task: "T010 [P] Create src/social/login_helper.py for manual session setup"
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T011)
3. Complete Phase 3: User Story 1 (T012-T021) - Orchestrator skeleton
4. Complete Phase 4: User Story 2 (T022-T031) - Meta Poster
5. **STOP and VALIDATE**: Test with LinkedIn + Meta only
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 2 (Meta) → Test independently → Deploy/Demo (MVP!)
3. Add User Story 3 (Twitter) → Test independently → Deploy/Demo
4. Add User Story 1 (Orchestrator) → Test all 4 platforms → Deploy/Demo
5. Add User Story 4 (Ralph Wiggum) → Test error recovery → Deploy/Demo
6. Each story adds value without breaking previous stories

### Full Phase 3 Delivery

1. Complete all phases (T001-T062)
2. Run integration tests (T054-T058)
3. Validate all platforms post successfully
4. Mark Phase 3 as 'Closed' per Constitution Principle V
5. Ready for Phase 4 (Platinum: Cloud-Local sync, 24/7 triage)

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
| Phase 2 | Foundational | 5 tasks |
| Phase 3 | User Story 1 (Cross-Platform) | 10 tasks |
| Phase 4 | User Story 2 (Meta) | 10 tasks |
| Phase 5 | User Story 3 (Twitter) | 9 tasks |
| Phase 6 | User Story 4 (Ralph Wiggum) | 9 tasks |
| Phase 7 | Polish | 13 tasks |
| **Total** | | **62 tasks** |

**MVP Scope**: Phases 1-2 + US2 (T001-T031) = 31 tasks → Meta posting ready for demo
