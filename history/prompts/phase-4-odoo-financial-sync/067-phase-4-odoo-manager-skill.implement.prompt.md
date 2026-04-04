---
id: 067
title: phase-4-odoo-manager-skill
stage: implement
date: 2026-04-02T00:00:00Z
surface: agent
model: qwen-code
feature: odoo-financial-sync
branch: 001-odoo-financial-sync
user: Faiz
command: /sp.implement (phase-4-python-odoo-skill)
labels: ["implementation", "phase-4", "odoo", "python", "xml-rpc"]
links:
  spec: specs/001-odoo-financial-sync/spec.md
  plan: specs/001-odoo-financial-sync/plan.md
  tasks: specs/001-odoo-financial-sync/tasks.md
  ticket: null
  adr: null
  pr: null
files:
  - src/skills/odoo_manager.py (OdooManager class with authenticate, create_journal_entry, log_post_expense)
  - ODOO_ACCOUNT_SETUP.md (account setup guide)
tests:
  - python src/skills/odoo_manager.py (connection test)
---

## Prompt

/sp.implement { "phase": "phase-4-python-odoo-skill", "instructions": [ "1. CREATE FILE: In 'src/skills/odoo_manager.py', create a class 'OdooManager'.", "2. LIBRARY: Import 'xmlrpc.client'. This is the standard way to talk to Odoo from Python.", "3. CONNECT METHOD: Add 'authenticate()' that uses: - url = 'http://localhost:8069' - db = 'odoo_vault' - username = 'admin' - password = 'admin'", "4. LOG EXPENSE METHOD: Add 'log_post_expense(platform, cost=500)' that creates a 'Journal Entry' in Odoo with the description: 'Marketing Cost for [Platform] Post'.", "5. TEST SCRIPT: Create a small block at the end of the file to test the connection and print 'Odoo Connected Successfully!' in the terminal." ] }

## Response snapshot

Implemented Phase 4 Odoo Manager skill:

**Files Created**:
1. src/skills/odoo_manager.py - Complete OdooManager class with:
   - authenticate() - XML-RPC authentication, returns UID
   - check_connection() - Health check, verifies database access
   - create_journal_entry() - Creates account.move entries
   - log_post_expense() - High-level wrapper with error handling
   - Test script at bottom (runs when executed directly)

2. ODOO_ACCOUNT_SETUP.md - Guide to create Marketing Expense account

**Test Results**:
✅ Docker containers running (vault-db, vault-odoo)
✅ Odoo Connected Successfully!
✅ User ID (UID): 2
✅ Connection healthy - found 328 models
⚠️ Marketing Expense account 500000 needs to be created in Odoo

**Exit Criteria**:
✅ File 'src/skills/odoo_manager.py' created - COMPLETE
✅ Running the script prints User ID (UID) from Odoo - COMPLETE (UID: 2)

**Next Steps for User**:
1. Create Marketing Expense account in Odoo (see ODOO_ACCOUNT_SETUP.md)
   - Code: 500000
   - Name: Marketing Expense
   - Type: Expense
2. Run test again: python src/skills/odoo_manager.py
3. Verify journal entry created successfully
4. Proceed to integrate with social orchestrator

## Outcome

- ✅ Impact: Odoo Manager skill complete, connection verified
- 🧪 Tests: Connection test passes (UID: 2)
- 📁 Files: 2 files created (odoo_manager.py, account setup guide)
- 🔁 Next prompts: Create marketing account in Odoo, then integrate with orchestrator
- 🧠 Reflection: XML-RPC connection working, just need account setup in Odoo UI

## Evaluation notes (flywheel)

- Failure modes observed: Account 500000 doesn't exist yet (expected, needs manual setup)
- Graders run and results: Test script executed successfully
- Prompt variant: Phase 4 Odoo Manager skill implementation
- Next experiment: Create account in Odoo, run test again, verify journal entry created
