---
id: 014
title: phase-2-gmail-auth-fixes
stage: implement
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-2-functional
branch: 002-phase-2-functional
user: Faiz
command: /sp.implement (gmail auth fixes)
labels: ["implementation", "phase-2", "gmail", "authentication", "bug-fix"]
links:
  spec: specs/002-phase-2-functional/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/gmail/gmail_auth.py (updated)
  - src/gmail/gmail_sender.py (updated)
tests:
  - N/A (implementation phase)
---

## Prompt

/sp.implement { "phase": "phase-2-functional", "instructions": [ "1. In 'src/gmail/gmail_auth.py', add a line at the very beginning of the authenticate function to manually delete 'token.json' if it exists. This will force a new browser window.", "2. Fix the SCOPES variable in the script to be exactly: ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.send']", "3. Ensure the script looks for 'credentials.json' (the one from Google Cloud Console) to start the flow.", "4. Update 'gmail_sender.py' to print a clear 'SUCCESS: Email Sent' message when the API call works." ] }

## Response snapshot

Fixed Gmail authentication and sender issues:

**Fixes Applied**:
1. ✓ token.json deletion: Added at start of authenticate_gmail() to force new browser auth
2. ✓ SCOPES: Already correct ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.send']
3. ✓ credentials.json: Script already looks for credentials.json from Google Cloud Console
4. ✓ SUCCESS message: Added clear "SUCCESS: Email Sent!" output with To, Subject, Message ID

**Files Updated**:
1. src/gmail/gmail_auth.py - Added token.json deletion logic
2. src/gmail/gmail_sender.py - Added SUCCESS message

**Exit Criteria**:
✅ Running authenticate command MUST open browser window - FIXED (token.json deleted)

**Tasks Updated**:
- T071: Delete token.json to force auth ✓
- T072: SCOPES verification ✓ (already correct)
- T073: SUCCESS message added ✓

**Usage**:
```bash
# Force new authentication (will open browser)
python src/gmail/gmail_auth.py --authenticate

# Test Gmail connection
python src/gmail/gmail_auth.py --test
```

**Expected Output** (on auth):
```
[Auth] Deleting existing token.json to force new authentication...
[Auth] Deleted: E:\...\token.json

Starting OAuth2 authentication flow...
This will open a browser window for Google login
```

**Expected Output** (on send):
```
============================================================
SUCCESS: Email Sent!
============================================================
To: recipient@example.com
Subject: Re: Original Subject
Message ID: 18f3a2b1c4d5e6f7
============================================================
```

## Outcome

- ✅ Impact: Gmail auth now forces browser window, clear SUCCESS feedback
- 🧪 Tests: N/A (implementation - manual testing required)
- 📁 Files: 2 files updated
- 🔁 Next prompts: Run 'python src/gmail/gmail_auth.py --authenticate' to test
- 🧠 Reflection: SCOPES were already correct; main fix was token.json deletion

## Evaluation notes (flywheel)

- Failure modes observed: Browser not opening (fixed by token.json deletion)
- Graders run and results: N/A (pending user to test authentication)
- Prompt variant: Gmail authentication bug fixes
- Next experiment: Test auth flow, verify browser opens, test email sending
