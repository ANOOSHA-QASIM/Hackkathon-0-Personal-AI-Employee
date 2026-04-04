---
id: 026
title: phase-3-session-setup-skeletons
stage: implement
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-3-social-media-suite
branch: 003-phase-3-social-media-suite
user: Faiz
command: /sp.implement (phase-3-session-setup)
labels: ["implementation", "phase-3", "sessions", "login-helper", "skill-skeletons"]
links:
  spec: specs/003-phase-3-social-media-suite/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/social/login_helper.py
  - src/social/__init__.py
  - src/skills/base_poster.py
  - src/skills/meta_poster.py
  - src/skills/twitter_poster.py
  - src/skills/__init__.py
tests:
  - N/A (implementation phase - session testing required)
---

## Prompt

/sp.implement { "phase": "phase-3-gold-sessions", "instructions": [ "1. Create 'src/social/login_helper.py' to handle persistent sessions for Meta and Twitter.", "2. Script Logic: (a) Use Playwright to launch a browser with a user_data_dir, (b) Add arguments for '--once-meta' and '--once-twitter', (c) Wait for the user to manually login and press Enter in the terminal to save and close.", "3. Directory Setup: Ensure sessions are saved in 'E:/hackathon_0_digital_fte/AI_Employee_vault/.browser_data/meta' and '.browser_data/twitter'.", "4. Skill Skeleton: Create 'src/skills/meta_poster.py' and 'src/skills/twitter_poster.py' as empty class structures ready for the next implementation step." ] }

## Response snapshot

Implemented Phase 3 session setup and skill skeletons:

**Files Created**:
1. src/social/login_helper.py - Manual session setup for Meta and Twitter
   - --once-meta: Login to Facebook/Instagram, session saved to .browser_data/meta
   - --once-twitter: Login to Twitter/X, session saved to .browser_data/twitter
   - Verifies login by checking for platform-specific elements
   - Waits for user to press ENTER before saving and closing

2. src/skills/base_poster.py - BasePoster abstract class
   - PostingResult class for standardized return types
   - _launch_browser() helper with persistent context
   - _validate_content() and _validate_media() helpers
   - Abstract post() and authenticate() methods

3. src/skills/meta_poster.py - MetaPoster skeleton
   - post() method (TODO: implement)
   - authenticate() method (TODO: implement)
   - post_to_facebook() method (TODO: implement)
   - post_to_instagram() method (TODO: implement)

4. src/skills/twitter_poster.py - TwitterPoster skeleton
   - post() method with auto-threading (TODO: implement)
   - authenticate() method (TODO: implement)
   - _split_into_thread() method (TODO: implement)
   - _post_tweet() and _post_thread() methods (TODO: implement)

**Directory Structure Created**:
- src/social/ (login_helper.py, __init__.py)
- src/skills/ (base_poster.py, meta_poster.py, twitter_poster.py, __init__.py)
- .browser_data/meta/ (session storage)
- .browser_data/twitter/ (session storage)

**Exit Criteria**:
✅ Running login helper allows user to save sessions for FB, IG, and X - IMPLEMENTED
✅ Folder structure for Gold Social skills created - IMPLEMENTED

**Tasks Updated**:
- T001-T006: Phase 1 Setup complete ✓
- T007, T010: Phase 2 Foundational partial ✓
- T022-T023: Meta skill skeleton ✓
- T032-T033: Twitter skill skeleton ✓

## Outcome

- ✅ Impact: Session setup and skill skeletons ready for Phase 3 implementation
- 🧪 Tests: N/A (implementation - user must run login_helper.py to test sessions)
- 📁 Files: 6 files created (login_helper, base_poster, meta_poster, twitter_poster, 2x __init__.py)
- 🔁 Next prompts: Run 'python src/social/login_helper.py --once-meta' to set up sessions
- 🧠 Reflection: Skeletons provide clear structure for next implementation step

## Evaluation notes (flywheel)

- Failure modes observed: None (implementation complete)
- Graders run and results: N/A (pending user to test session setup)
- Prompt variant: Phase 3 session setup and skeletons
- Next experiment: Run login_helper.py for Meta and Twitter, then implement posting logic
