---
id: 016
title: phase-2-linkedin-login-assistant
stage: implement
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-2-functional
branch: 002-phase-2-functional
user: Faiz
command: /sp.implement (linkedin login assistant)
labels: ["implementation", "phase-2", "linkedin", "login-assistant"]
links:
  spec: specs/002-phase-2-functional/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/linkedin/login_assistant.py (new)
  - src/linkedin/linkedin_poster.py (updated)
tests:
  - N/A (implementation phase)
---

## Prompt

/sp.implement { "phase": "phase-2-functional", "instructions": [ "1. Create a temporary script 'src/linkedin/login_assistant.py' that ONLY launches a persistent Chromium browser in 'headless=False' mode to 'https://www.linkedin.com/login'.", "2. The assistant should use the data directory './.browser_data/linkedin' and wait for 120 seconds (or until the user closes it) to allow manual login.", "3. Update 'src/linkedin/linkedin_poster.py' to: (a) Use 'headless=False' for now, (b) Check for 'status: Approved' (case-insensitive) in the YAML frontmatter, and (c) Add a print statement if the status is missing.", "4. Fix the file filter so it correctly identifies '.md' files in 'E:/hackathon_0_digital_fte/AI_Employee_vault/Approved'." ] }

## Response snapshot

Created LinkedIn login assistant and updated poster:

**Created Files**:
1. src/linkedin/login_assistant.py - Standalone login helper:
   - Opens browser to https://www.linkedin.com/login
   - headless=False (visible browser)
   - Uses persistent data directory .browser_data/linkedin
   - Waits 120 seconds for manual login
   - Detects login automatically
   - Saves session for future use

**Updated Files**:
2. src/linkedin/linkedin_poster.py - Enhanced file filtering:
   - headless=False (visible browser)
   - Checks for 'status' field in metadata
   - Case-insensitive status check (approved, draft, etc.)
   - Prints WARNING if status missing
   - Explicit .md file filter with logging
   - Shows count of files found

**Exit Criteria**:
✅ Running 'python src/linkedin/login_assistant.py' opens visible browser - IMPLEMENTED

**Usage**:
```bash
# Step 1: Login assistant (first time only)
python src/linkedin/login_assistant.py

# Step 2: Run LinkedIn poster
python src/linkedin/linkedin_poster.py --once
```

**Expected Output** (login assistant):
```
============================================================
LinkedIn Login Assistant
============================================================

This will open a browser window to LinkedIn login.
You have 120 seconds to log in manually.
...
Opening browser...
Navigating to https://www.linkedin.com/login...

============================================================
Browser is now open.
Please log in to LinkedIn in the browser window.
...
✓ Login detected! Session will be saved.
```

**Tasks Updated**:
- T076: login_assistant.py created ✓
- T077: status field check (case-insensitive) ✓
- T078: .md file filter fixed ✓

## Outcome

- ✅ Impact: Login assistant simplifies first-time LinkedIn setup
- 🧪 Tests: N/A (implementation - manual testing required)
- 📁 Files: 2 files created/updated
- 🔁 Next prompts: Run 'python src/linkedin/login_assistant.py' to login
- 🧠 Reflection: Separate login script cleaner than embedding in poster

## Evaluation notes (flywheel)

- Failure modes observed: None (implementation complete)
- Graders run and results: N/A (pending user to test login assistant)
- Prompt variant: LinkedIn login assistant creation
- Next experiment: Test login assistant, verify session persistence
