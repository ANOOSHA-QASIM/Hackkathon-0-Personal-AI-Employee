---
id: 008
title: phase-2-functional-tasks-generation
stage: tasks
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-2-functional
branch: 002-phase-2-functional
user: Faiz
command: /sp.tasks
labels: ["tasks", "phase-2", "functional", "gmail", "linkedin", "hitl"]
links:
  spec: specs/002-phase-2-functional/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-phase-2-functional/tasks.md
tests:
  - N/A (task generation phase)
---

## Prompt

/sp.tasks { "phase": "phase-2-functional", "task_list": [ { "id": "T2.1", "description": "Configure Gmail MCP to fetch unread emails and save them as JSON in /Logs/Temp.", "priority": "high" }, { "id": "T2.2", "description": "Develop 'Triage_Processor.py' to convert Gmail JSON into .md files in /Needs_Action with 'type: email' metadata.", "priority": "high" }, { "id": "T2.3", "description": "Set up Playwright MCP to navigate to LinkedIn.com and perform a 'Login Check' (Headed mode).", "priority": "high" }, { "id": "T2.4", "description": "Create a 'LinkedIn_Template.md' in /Briefings with placeholders for [Headline], [Body], and [Tags].", "priority": "medium" }, { "id": "T2.5", "description": "Write a 'Post_Executor.py' that watches /Approved/LinkedIn, reads the .md content, and posts it via Playwright.", "priority": "high" }, { "id": "T2.6", "description": "Add a 'Social Media Queue' table to Dashboard.md to track Status (Draft/Approved/Posted).", "priority": "low" } ], "verification_method": "Send a test email to yourself and check if a task appears in /Needs_Action. Then, move a draft to /Approved and verify the LinkedIn post." }

## Response snapshot

Generated tasks.md with 59 tasks organized by 4 user stories for independent implementation:

**Phase Structure**:
- Phase 1: Setup (6 tasks) - Directory structure, dependencies, Playwright browser install
- Phase 2: Foundational (6 tasks) - Gmail OAuth2, processed_emails.json, audit logger extension
- Phase 3: US1 Gmail Alerts (8 tasks) - gmail_watcher.py, email_processor.py, alert creation
- Phase 4: US2 LinkedIn HITL (11 tasks) - post_generator.py, linkedin_publisher.py, Playwright automation
- Phase 5: US3 Triage (8 tasks) - communication_triage.py, keyword matching, VIP sender logic
- Phase 6: US4 Metadata (8 tasks) - post_scheduler.py, metadata validation, scheduled publishing
- Phase 7: Polish (12 tasks) - README, batch files, integration tests, Dashboard update

**Key Features**:
- Tasks organized by user story (US1, US2, US3, US4) for independent implementation
- [P] markers for parallelizable tasks (different files, no dependencies)
- Exact file paths for all tasks (src/gmail/, src/linkedin/, src/triage/)
- MVP scope identified: Phases 1-3 (20 tasks) → Gmail alerts ready for demo
- Parallel opportunities documented per phase
- Implementation strategy: MVP first, incremental delivery, parallel team options

**Task Format Compliance**:
- All tasks follow: `- [ ] T### [P?] [US?] Description with file path`
- Checkbox format: ✅
- Sequential IDs: ✅
- Story labels (US1-US4): ✅
- File paths included: ✅

**User Task Mapping**:
- T2.1 → T013-T014 (Gmail watcher)
- T2.2 → T015-T017 (email processor)
- T2.3 → T024-T025 (LinkedIn Playwright)
- T2.4 → T023 (LinkedIn template)
- T2.5 → T026-T029 (post publisher)
- T2.6 → T058 (Dashboard update)

## Outcome

- ✅ Impact: 59 implementation tasks generated, organized by 4 user stories, ready for execution
- 🧪 Tests: N/A (task generation - tests optional per spec)
- 📁 Files: specs/002-phase-2-functional/tasks.md
- 🔁 Next prompts: /sp.implement to start coding, or manual task-by-task execution
- 🧠 Reflection: User provided 6 sample tasks → expanded to 59 comprehensive tasks covering all 4 user stories from spec

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results: Task format validation - all tasks follow checklist format
- Prompt variant: Task generation from plan + spec + user tasks
- Next experiment: Begin implementation with /sp.implement or manual task execution
