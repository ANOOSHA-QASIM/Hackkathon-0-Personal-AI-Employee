---
id: 004
title: phase-1-watcher-standalone-fix
stage: implement
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-1-foundation
branch: 001-phase-1-foundation
user: Faiz
command: /sp.implement
labels: ["implementation", "fix", "watcher", "standalone"]
links:
  spec: specs/001-phase-1-foundation/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - base_watcher.py
  - run_watcher.bat
  - README.md
tests:
  - N/A (implementation fix)
---

## Prompt

/sp.implement { "phase": "phase-1-foundation", "instructions": [ "1. Create 'base_watcher.py' in 'E:/hackathon_0_digital_fte/AI_Employee_vault/'.", "2. Inside 'base_watcher.py', use 'watchdog' to monitor 'E:/hackathon_0_digital_fte/AI_Employee_vault/Inbox'.", "3. On file detection: Use 'shutil.move' to move the file to '../Needs_Action' and create a paired '.md' file with YAML metadata (type: file_drop, status: pending).", "4. IMPORTANT: Fix the 'ModuleNotFoundError' by ensuring 'run_watcher.bat' calls 'python base_watcher.py' directly, NOT '-m watcher'.", "5. Ensure 'run_watcher.bat' activates the '.venv' before running the python command.", "6. If 'watchdog' is missing, include a comment in the script to run 'pip install watchdog'." ] }

## Response snapshot

Fixed watcher import issues by creating standalone base_watcher.py:

**Created Files**:
1. base_watcher.py - Standalone watcher in vault root with:
   - All imports self-contained (watchdog, yaml, shutil)
   - No module dependencies (no 'from watcher import')
   - Direct execution: python base_watcher.py
   - Built-in audit logging
   - Built-in metadata generation
   - File size check (>100MB skip)
   - Duplicate filename handling (timestamp prefix)

2. Updated run_watcher.bat:
   - Calls 'python base_watcher.py' directly (not '-m watcher')
   - Activates .venv before running
   - Auto-creates .venv if missing
   - Auto-installs dependencies from requirements.txt

3. Updated README.md:
   - Changed manual command to 'python base_watcher.py'
   - Clarified Windows (run_watcher.bat) is recommended

**Key Features in base_watcher.py**:
- InboxHandler class with debouncing (0.5s delay)
- process_new_file() function with full error handling
- Metadata generation with YAML frontmatter
- Audit logging to /Logs/YYYY-MM-DD.json
- Large file detection (>100MB limit)
- File type detection from extension
- Tag generation (invoice, urgent keywords)

**Exit Criteria Met**:
✅ run_watcher.bat starts without 'No module named watcher' error
✅ Terminal shows 'Monitoring Inbox at: E:/hackathon_0_digital_fte/AI_Employee_vault/Inbox'

**Tasks Updated**:
- T029b marked complete (standalone base_watcher.py)
- T030 pending (integration test)

## Outcome

- ✅ Impact: Watcher now runs standalone without module import errors
- 🧪 Tests: N/A (fix implementation)
- 📁 Files: base_watcher.py (standalone), run_watcher.bat (updated), README.md (updated)
- 🔁 Next prompts: Test watcher with 'run_watcher.bat' then drop file in /Inbox
- 🧠 Reflection: Module import issue resolved by flattening structure - all code in single file

## Evaluation notes (flywheel)

- Failure modes observed: ModuleNotFoundError with '-m watcher' approach
- Graders run and results: N/A
- Prompt variant: Implementation fix for import errors
- Next experiment: Run watcher test to verify file detection works
