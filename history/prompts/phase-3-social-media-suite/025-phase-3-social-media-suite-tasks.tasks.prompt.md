---
id: 025
title: phase-3-social-media-suite-tasks
stage: tasks
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-3-social-media-suite
branch: 003-phase-3-social-media-suite
user: Faiz
command: /sp.tasks
labels: ["tasks", "phase-3", "social-media", "meta", "twitter", "gold-tier"]
links:
  spec: specs/003-phase-3-social-media-suite/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-phase-3-social-media-suite/tasks.md
tests:
  - N/A (task generation phase)
---

## Prompt

/sp.tasks { "goal": "Implement Meta (FB/IG) and Twitter (X) Agent Skills", "context": "Phase 3 Gold Tier - Multi-platform social media expansion following the approved Plan.", "tasks": [ "1. SESSION SETUP: Create 'src/social/login_helper.py' to manually save persistent browser sessions for Meta (Facebook/Instagram) and X (Twitter) in '.browser_data/'.", "2. META SKILL: Develop 'src/skills/meta_poster.py' using Playwright to: (a) Navigate to FB/IG, (b) Upload media from metadata, (c) Type caption, (d) Click Publish.", "3. X SKILL: Develop 'src/skills/twitter_poster.py' using Playwright to: (a) Navigate to x.com, (b) Handle 'Post' button, (c) Handle character limits and media.", "4. MASTER DISPATCHER: Create 'src/skills/social_orchestrator.py' that watches '/Approved/Social' and triggers LinkedIn, Meta, and X skills in parallel or sequence.", "5. RALPH WIGGUM LOOP: Implement a basic 'try-except-retry' wrapper in the orchestrator to retry failed platforms 3 times with a 5-minute cooldown.", "6. DOCUMENTATION: Update 'Handbook.md' with instructions on how to approve a single post for all 4 platforms." ] }

## Response snapshot

Generated tasks.md with 62 tasks organized by 4 user stories for independent implementation:

**Phase Structure**:
- Phase 1: Setup (6 tasks) - Directory structure, __init__.py files, folders
- Phase 2: Foundational (5 tasks) - BasePoster class, config extension, Ralph Wiggum base, login helper
- Phase 3: US1 Cross-Platform (10 tasks) - Social Dispatcher, platform integration, status tracking
- Phase 4: US2 Meta (10 tasks) - MetaPoster class, Facebook/Instagram posting, image handling
- Phase 5: US3 Twitter (9 tasks) - TwitterPoster class, auto-threading, image attachment
- Phase 6: US4 Ralph Wiggum (9 tasks) - Error recovery, 15-min cooldown, escalation
- Phase 7: Polish (13 tasks) - Documentation, batch files, integration tests

**Key Features**:
- Tasks organized by user story (US1, US2, US3, US4) for independent implementation
- [P] markers for parallelizable tasks (different files, no dependencies)
- Exact file paths for all tasks (src/skills/, src/orchestrator/, src/utils/)
- MVP scope identified: Phases 1-2 + US2 (31 tasks) → Meta posting ready for demo
- Parallel opportunities documented per phase
- Implementation strategy: MVP first, incremental delivery, parallel team options

**Task Format Compliance**:
- All tasks follow: `- [ ] T### [P?] [US?] Description with file path`
- Checkbox format: ✅
- Sequential IDs: ✅
- Story labels (US1-US4): ✅
- File paths included: ✅

**User Task Mapping**:
- Task 1 (Session Setup) → T010 (login_helper.py)
- Task 2 (Meta Skill) → T022-T031 (meta_poster.py)
- Task 3 (X Skill) → T032-T040 (twitter_poster.py)
- Task 4 (Master Dispatcher) → T012-T021 (social_dispatcher.py)
- Task 5 (Ralph Wiggum) → T041-T049 (ralph_wiggum.py + integration)
- Task 6 (Documentation) → T051 (Handbook.md update)

## Outcome

- ✅ Impact: 62 implementation tasks generated, organized by 4 user stories, ready for execution
- 🧪 Tests: N/A (task generation - tests optional per spec)
- 📁 Files: specs/003-phase-3-social-media-suite/tasks.md
- 🔁 Next prompts: /sp.implement to start coding, or manual task-by-task execution
- 🧠 Reflection: User provided 6 sample tasks → expanded to 62 comprehensive tasks covering all 4 user stories from spec

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results: Task format validation - all tasks follow checklist format
- Prompt variant: Task generation from plan + spec + user tasks
- Next experiment: Begin implementation with /sp.implement or manual task execution
