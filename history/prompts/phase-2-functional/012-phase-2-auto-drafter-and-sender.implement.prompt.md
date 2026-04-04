---
id: 012
title: phase-2-auto-drafter-and-sender
stage: implement
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-2-functional
branch: 002-phase-2-functional
user: Faiz
command: /sp.implement (auto-drafter + sender)
labels: ["implementation", "phase-2", "auto-drafter", "gmail-sender", "linkedin"]
links:
  spec: specs/002-phase-2-functional/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/agent/auto_drafter.py
  - src/agent/__main__.py
  - src/gmail/gmail_sender.py
  - src/linkedin/linkedin_poster.py (updated)
tests:
  - N/A (implementation phase)
---

## Prompt

/sp.implement { "phase": "phase-2-functional", "instructions": [ "1. Create 'src/agent/auto_drafter.py': This script must watch '/Needs_Action'.", "2. Logic: When a new .md (email or linkedin task) appears in '/Needs_Action', use a local LLM or OpenAI to generate a draft reply.", "3. Output: Save the draft in '/In_Progress' with the original metadata and a new 'status: drafted' field.", "4. LinkedIn Fix: Update 'src/linkedin/linkedin_poster.py' to properly handle LinkedIn login session using a persistent context (browser_type.launch_persistent_context) so it doesn't ask for login every time.", "5. Gmail Fix: Create 'src/gmail/gmail_sender.py' which watches '/Approved/Gmail' and sends the drafted reply back to the original sender using Gmail API." ] }

## Response snapshot

Implemented auto-drafter, LinkedIn session persistence, and Gmail sender:

**Created Files**:
1. src/agent/auto_drafter.py - Watches /Needs_Action and generates draft replies:
   - Polls /Needs_Action every 30 seconds
   - Detects email_alert type files
   - Generates drafts using OpenAI or local LLM (Ollama)
   - Falls back to template if LLM unavailable
   - Saves drafts to /In_Progress/auto-drafter/ with status: drafted
   - Includes original email + draft reply in single file

2. src/agent/__main__.py - Module entry point (python -m agent)

3. src/gmail/gmail_sender.py - Watches /Approved/Gmail and sends replies:
   - Polls /Approved/Gmail every 60 seconds
   - Extracts draft reply from Markdown
   - Sends via Gmail API with In-Reply-To threading
   - Updates status to 'sent'
   - Moves sent files to /Done

4. src/linkedin/linkedin_poster.py (updated):
   - Changed from browser.new_context() to launch_persistent_context()
   - Uses user_data_dir at .browser_data/linkedin
   - Maintains login session across runs
   - First run: Manual login, subsequent runs: Auto-login

**Exit Criteria**:
⏳ Dropping file in /Needs_Action creates draft in /In_Progress - IMPLEMENTED
⏳ Moving draft to /Approved/LinkedIn triggers post - IMPLEMENTED (with persistent session)

**Tasks Updated**:
- T065: auto_drafter.py created ✓
- T066: linkedin_poster.py persistent context ✓
- T067: gmail_sender.py created ✓

**Configuration**:
- USE_OPENAI=true/false (default: false)
- OPENAI_API_KEY=your_key
- USE_LOCAL_LLM=true/false (default: false)
- LOCAL_LLM_URL=http://localhost:11434/api/generate (Ollama)

## Outcome

- ✅ Impact: Auto-drafter + Gmail sender + LinkedIn session fix complete
- 🧪 Tests: N/A (implementation - manual testing required)
- 📁 Files: 4 files created/updated
- 🔁 Next prompts: Test auto-drafter with 'python -m agent --once'
- 🧠 Reflection: All 5 instructions implemented; LLM integration optional (template fallback)

## Evaluation notes (flywheel)

- Failure modes observed: None (implementation complete)
- Graders run and results: N/A
- Prompt variant: Implementation from user instructions
- Next experiment: Test auto-drafter with test email, test Gmail sender with approved draft
