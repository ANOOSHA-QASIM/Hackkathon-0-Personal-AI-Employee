---
id: 015
title: phase-2-linkedin-browser-fix
stage: implement
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-2-functional
branch: 002-phase-2-functional
user: Faiz
command: /sp.implement (linkedin browser fix)
labels: ["implementation", "phase-2", "linkedin", "browser", "session"]
links:
  spec: specs/002-phase-2-functional/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/linkedin/linkedin_poster.py (updated)
tests:
  - N/A (implementation phase)
---

## Prompt

/sp.implement { "phase": "phase-2-functional", "instructions": [ "1. Update 'src/linkedin/linkedin_poster.py' to launch the browser in 'headless=False' mode temporarily.", "2. Add a 'time.sleep(60)' or a 'page.pause()' command after navigating to LinkedIn, so the user has time to manually log in.", "3. Ensure 'context = browser.launch_persistent_context(user_data_dir="./.browser_data/linkedin")' is used to save the session permanently.", "4. Change the logic to NOT skip files if they are in the '/Approved' folder and have 'platform: linkedin' metadata." ] }

## Response snapshot

Updated LinkedIn poster for proper browser login and session persistence:

**Changes Made**:
1. ✓ headless=False: Browser launches in visible mode for manual login
2. ✓ 60-second pause: Added time.sleep(60) after navigation for manual login
3. ✓ Persistent context: Already using launch_persistent_context with user_data_dir
4. ✓ File filtering: Already correctly processes files with platform: linkedin

**Files Updated**:
1. src/linkedin/linkedin_poster.py - Added 60s login pause, improved messaging

**Key Features**:
- Browser opens visibly (headless=False)
- Waits 60 seconds for manual login
- Additional 4-minute wait if not logged in initially
- Session saved to .browser_data/linkedin permanently
- Processes all /Approved files with platform: linkedin

**Exit Criteria**:
✅ A Chromium browser window opens, stays open for login, and saves the session - IMPLEMENTED

**Usage**:
```bash
# Run LinkedIn poster
python src/linkedin/linkedin_poster.py

# Or run once for testing
python src/linkedin/linkedin_poster.py --once
```

**Expected Flow**:
1. Browser opens (visible, headless=False)
2. Navigates to LinkedIn
3. Waits 60 seconds "Waiting for manual login if needed..."
4. User logs in (first time only)
5. Session saved to .browser_data/linkedin
6. Subsequent runs: Auto-logged in

**Tasks Updated**:
- T074: 60s login pause added ✓
- T075: Persistent context verified ✓

## Outcome

- ✅ Impact: LinkedIn poster now properly handles login and saves session
- 🧪 Tests: N/A (implementation - manual testing required)
- 📁 Files: 1 file updated
- 🔁 Next prompts: Test with 'python src/linkedin/linkedin_poster.py --once'
- 🧠 Reflection: Persistent context was already implemented; main fix was 60s pause

## Evaluation notes (flywheel)

- Failure modes observed: None (implementation complete)
- Graders run and results: N/A (pending user to test LinkedIn posting)
- Prompt variant: LinkedIn browser session fix
- Next experiment: Test LinkedIn post flow, verify session persistence across runs
