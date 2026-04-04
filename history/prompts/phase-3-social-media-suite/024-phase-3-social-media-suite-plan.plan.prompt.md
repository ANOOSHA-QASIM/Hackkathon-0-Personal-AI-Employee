---
id: 024
title: phase-3-social-media-suite-plan
stage: plan
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-3-social-media-suite
branch: 003-phase-3-social-media-suite
user: Faiz
command: /sp.plan
labels: ["plan", "phase-3", "social-media", "meta", "twitter", "gold-tier"]
links:
  spec: specs/003-phase-3-social-media-suite/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-phase-3-social-media-suite/plan.md
  - specs/003-phase-3-social-media-suite/research.md
  - specs/003-phase-3-social-media-suite/data-model.md
  - specs/003-phase-3-social-media-suite/quickstart.md
  - specs/003-phase-3-social-media-suite/contracts/social-media-post-schema.yaml
tests:
  - N/A (planning phase)
---

## Prompt

/sp.plan { "goal": "Phase 3 (Gold) - Multi-Platform Social Media Integration (Meta & X)", "context": "Phase 2 LinkedIn is complete. Now implementing Gold Tier requirements for Facebook, Instagram, and Twitter (X) as modular Agent Skills.", "tasks": [ "1. ARCHITECTURE: Update 'src/skills/' structure to accommodate 'meta_poster.py' and 'twitter_poster.py'.", "2. META SKILL: Develop Playwright-based posting for Facebook and Instagram (handling login sessions and image uploads).", "3. X (TWITTER) SKILL: Develop Playwright-based posting for X to handle short-form content and media.", "4. ORCHESTRATION: Create a 'Master Social Dispatcher' that detects files in '/Approved/Social' and triggers all active platforms.", "5. ERROR RECOVERY: Implement a basic 'Ralph Wiggum' retry loop for failed platform posts (90s timeouts and 3-retry limit)." ] }

## Response snapshot

Created implementation plan for Phase 3 Social Media Suite with:

**Technical Context**:
- Python 3.11+ with playwright, pyyaml, python-dotenv
- File-based state (Markdown + YAML frontmatter, browser sessions)
- Windows platform (E:/ drive)
- 95% posts to all 4 platforms within 10 minutes

**Constitution Check**: All 10 principles PASS
- I-X: All principles satisfied (Inbox-First, Schema Compliance, Claim-By-Move, HITL, Phase Lock, Audit Logging, Weekly Audit, Modular Skills, Ralph Wiggum, Minimalist Design)

**Phase 0 Research** (5 decisions):
1. Playwright for Meta (Facebook + Instagram) - consistent, no API approval
2. Playwright for Twitter - consistent, auto-threading support
3. 280-char split with "..." - standard threading pattern
4. .browser_data/ per platform - persistent sessions
5. 15-min cooldown, 3 retries, escalate - Ralph Wiggum recovery

**Phase 1 Artifacts**:
- data-model.md: SocialMediaPost, PlatformSkill, PostingResult, RalphWiggumState, PersistentSession
- contracts/: social-media-post-schema.yaml
- quickstart.md: Setup guide, platform notes, troubleshooting

**Source Structure**:
src/skills/ (meta_poster.py, twitter_poster.py, base_poster.py)
src/orchestrator/ (social_dispatcher.py)
src/utils/ (ralph_wiggum.py)
tests/contract/, tests/integration/, tests/unit/

**Next Steps**: Ready for /sp.tasks to break into implementation tasks

## Outcome

- ✅ Impact: Plan complete for Phase 3 Social Media Suite (4 platforms, Ralph Wiggum recovery)
- 🧪 Tests: N/A (planning phase - tests will be created in /sp.tasks)
- 📁 Files: 5 planning documents created in specs/003-phase-3-social-media-suite/
- 🔁 Next prompts: /sp.tasks for implementation task breakdown
- 🧠 Reflection: All research decisions align with Constitution; no clarifications needed

## Evaluation notes (flywheel)

- Failure modes observed: None (planning phase)
- Graders run and results: Constitution Check - all 10 principles PASS
- Prompt variant: Planning from spec + user tasks
- Next experiment: Proceed to /sp.tasks for task breakdown
