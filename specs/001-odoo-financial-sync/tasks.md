# Implementation Tasks: Dockerized Odoo AI Accountant

**Feature Branch**: `001-odoo-financial-sync`
**Created**: 2026-03-28
**Spec**: [spec.md](spec/spec.md)
**Plan**: [plan.md](plan.md)
**Phase**: Phase 4 - Implementation Tasks

---

## Task Summary

**Total Tasks**: 18 tasks across 6 phases

**Tasks by Phase**:
- Phase 1 (Setup): 2 tasks
- Phase 2 (Foundational): 2 tasks
- Phase 3 (US1 - Automated Expense Logging): 6 tasks
- Phase 4 (US2 - Secure Config): 2 tasks
- Phase 5 (US3 - Docker Infrastructure): 3 tasks
- Phase 6 (US4 - Dynamic Costing): 2 tasks
- Phase 7 (Polish): 1 task

**Parallel Opportunities**: 8 tasks marked [P] can run in parallel

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 (User Story 1 only) - Core expense logging functionality

---

## Dependency Graph

```
Phase 1: Setup (T001-T002)
    ↓
Phase 2: Foundational (T003-T004)
    ↓
Phase 3: US1 - Automated Expense Logging (T005-T010) [P1 - Core Value]
    ↓
Phase 4: US2 - Secure Config (T011-T012) [P2 - Security]
    ↓
Phase 5: US3 - Docker Infrastructure (T013-T015) [P3 - DevOps]
    ↓
Phase 6: US4 - Dynamic Costing (T016-T017) [P4 - Finance Flexibility]
    ↓
Phase 7: Polish (T018)
```

**User Story Completion Order**:
1. US1 (P1): Automated Marketing Expense Logging - Core business value
2. US2 (P2): Secure Configuration - Security foundation
3. US3 (P3): Docker Infrastructure - Production deployment
4. US4 (P4): Dynamic Costing - Finance flexibility

---

## Phase 1: Setup (Project Initialization)

**Goal**: Prepare project structure and verify prerequisites

**Independent Test**: Can run `docker --version` and `docker-compose --version` successfully

### Tasks

- [ ] T001 Verify Docker Desktop is installed and running
  - Run: `docker --version` and `docker-compose --version`
  - Ensure Docker Desktop is running (check system tray)
  - File: System verification

- [ ] T002 [P] Create project directory structure
  - Create: `specs/001-odoo-financial-sync/` (already exists from planning)
  - Create: `src/skills/` (verify exists from Phase 3)
  - Create: `Logs/` (verify exists from Phase 3)
  - Files: Directory structure

---

## Phase 2: Foundational (Blocking Prerequisites)

**Goal**: Establish infrastructure and configuration foundation

**Independent Test**: Can access `http://localhost:8069` in browser after Docker start

### Tasks

- [ ] T003 Create docker-compose.yml in project root
  - Define `db` service: `postgres:15` with volume `odoo-postgres-data:/var/lib/postgresql/data`
  - Define `odoo` service: `odoo:17.0` with ports `8069:8069`, depends_on `db`, volume `odoo-web-data:/var/lib/odoo`
  - Add volumes section at bottom
  - File: `docker-compose.yml`

- [ ] T004 [P] Create .env.example template
  - Include: `ODOO_URL=http://localhost:8069`
  - Include: `ODOO_DB=odoo_vault`
  - Include: `ODOO_USER=admin`
  - Include: `ODOO_PASSWORD=admin`
  - Include: `ODOO_MARKETING_ACCOUNT=500000`
  - Include: `ODOO_BASE_COST=500`
  - File: `.env.example`

---

## Phase 3: User Story 1 - Automated Marketing Expense Logging (P1)

**Goal**: Core functionality - automatically log marketing expenses to Odoo after each post

**Independent Test**: After running social orchestrator with a test post, verify journal entry appears in Odoo with correct amount (500 PKR) and description

### Tasks

- [ ] T005 [P] [US1] Install python-dotenv package
  - Run: `pip install python-dotenv`
  - Add to requirements.txt if exists
  - File: `requirements.txt`

- [ ] T006 [P] [US1] Create src/skills/odoo_manager.py skeleton
  - Import: `xmlrpc.client`, `os`, `dotenv`
  - Define class: `OdooManager`
  - Add `__init__` method: Load env vars, initialize `self.url`, `self.db`, `self.uid`, `self.password`
  - File: `src/skills/odoo_manager.py`

- [ ] T007 [US1] Implement authenticate() method
  - Use `xmlrpc.client.ServerProxy` to connect to `{ODOO_URL}/xmlrpc/2/common`
  - Call `authenticate(db, username, password, {})`
  - Store returned uid in `self.uid`
  - Return bool (True if uid > 0)
  - File: `src/skills/odoo_manager.py`

- [ ] T008 [US1] Implement check_connection() method
  - Call `authenticate()` internally
  - Return bool indicating connection health
  - Add timeout handling (30 seconds)
  - File: `src/skills/odoo_manager.py`

- [ ] T009 [US1] Implement create_journal_entry() method
  - Connect to `{ODOO_URL}/xmlrpc/2/object`
  - Create `account.move` with:
    - `move_type`: "entry"
    - `name`: "Marketing Expense - {platform} - {timestamp}"
    - `date`: Current date
    - `line_ids`: [(0, 0, {account_id: 500000, debit: 500, name: "Marketing Expense"}), (0, 0, {account_id: 100000, credit: 500, name: "Cash/Bank"})]
    - `ref`: "Social Post: {post_title}"
    - `state`: "posted"
  - Return dict with `move_id` and status
  - File: `src/skills/odoo_manager.py`

- [ ] T010 [US1] Implement log_post_expense() wrapper method
  - Wrap `create_journal_entry()` with try/except
  - Log warning if Odoo unavailable (don't raise exception)
  - Return dict if successful, None if failed
  - Add audit logging to `/Logs/social_audit.json`
  - File: `src/skills/odoo_manager.py`

---

## Phase 4: User Story 2 - Secure Odoo Configuration (P2)

**Goal**: Secure credential management via environment variables

**Independent Test**: Verify no hardcoded credentials in source code; system reads from .env successfully

### Tasks

- [ ] T011 [P] [US2] Create .env file from .env.example
  - Copy `.env.example` to `.env`
  - Update credentials if different from defaults
  - Add `.env` to `.gitignore` (verify it's ignored)
  - Files: `.env`, `.gitignore`

- [ ] T012 [US2] Integrate dotenv loading in odoo_manager.py
  - Add `from dotenv import load_dotenv`
  - Call `load_dotenv()` in `__init__`
  - Use `os.getenv()` for all credential access
  - Add validation: raise error if required env vars missing
  - File: `src/skills/odoo_manager.py`

---

## Phase 5: User Story 3 - Docker Infrastructure Setup (P3)

**Goal**: Production-ready Docker deployment with data persistence

**Independent Test**: Run `docker-compose up -d`, verify both containers show "Up (healthy)" status, data persists after restart

### Tasks

- [ ] T013 [P] [US3] Start Odoo containers
  - Run: `docker-compose up -d`
  - Verify: `docker-compose ps` shows both containers "Up"
  - Access: `http://localhost:8069` in browser
  - Command: `docker-compose up -d`

- [ ] T014 [US3] Initialize Odoo database
  - Open browser: `http://localhost:8069`
  - Create database: `odoo_vault`
  - Set admin password: `admin`
  - Manual step: Browser UI interaction

- [ ] T015 [US3] Install Invoicing module
  - Navigate to: Apps menu
  - Search: "Invoicing"
  - Click: "Install" button
  - Wait for installation complete
  - Verify: Invoicing app appears in main dashboard
  - Manual step: Browser UI interaction

---

## Phase 6: User Story 4 - Dynamic Cost Per Post (P4)

**Goal**: Configurable base cost for marketing expenses

**Independent Test**: Change ODOO_BASE_COST in .env, verify new posts use updated amount

### Tasks

- [ ] T016 [P] [US4] Make base cost configurable in odoo_manager.py
  - Read `ODOO_BASE_COST` from env in `__init__`
  - Use `self.base_cost` in `create_journal_entry()` instead of hardcoded 500
  - Add validation: ensure cost is positive number
  - File: `src/skills/odoo_manager.py`

- [ ] T017 [US4] Update .env.example with cost configuration notes
  - Add comment: `# Base cost per social media post in PKR`
  - Add example values: 500, 750, 1000
  - File: `.env.example`

---

## Phase 7: Polish & Cross-Cutting Concerns

**Goal**: Documentation and integration verification

**Independent Test**: Can follow README to setup Odoo and run full test

### Tasks

- [ ] T018 [P] Update README.md with Odoo setup instructions
  - Add section: "Phase 4: Odoo Financial Integration"
  - Include: Docker start command
  - Include: Database setup steps
  - Include: Invoicing module installation
  - Include: .env configuration
  - Include: Test verification steps
  - File: `README.md`

---

## Parallel Execution Opportunities

**Group A - Infrastructure (Phase 1-2)**:
- T001 (Docker verify) + T002 (directory structure) → Can run in parallel
- T003 (docker-compose.yml) + T004 (.env.example) → Can run in parallel

**Group B - Odoo Skill Development (Phase 3)**:
- T005 (install dotenv) + T006 (skeleton) → Can run in parallel
- T007-T010 → Sequential (each method builds on previous)

**Group C - Configuration (Phase 4)**:
- T011 (.env file) + T012 (dotenv integration) → Sequential (T012 needs T011)

**Group D - Docker Setup (Phase 5)**:
- T013 (start containers) + T014 (DB init) + T015 (module install) → Sequential (UI steps depend on containers running)

**Group E - Cost Config (Phase 6)**:
- T016 (configurable cost) + T017 (docs) → Can run in parallel

**Group F - Documentation (Phase 7)**:
- T018 (README update) → Can run in parallel after all other phases complete

---

## Implementation Strategy

### MVP Scope (Phases 1-3)

**Minimum Viable Product**: Automated expense logging with hardcoded credentials and default cost

**Includes**:
- Docker infrastructure (T003)
- OdooManager skill with all methods (T006-T010)
- Basic integration (implicit in T010)

**Excludes** (deferred):
- Secure env management (Phase 4)
- Production Docker setup (Phase 5 UI steps)
- Configurable cost (Phase 6)
- Documentation polish (Phase 7)

**MVP Test**: Run social orchestrator with test post → Verify Odoo entry created

### Incremental Delivery

**Increment 1** (Phases 1-3): Core functionality works with hardcoded config
**Increment 2** (Phase 4): Secure credential management
**Increment 3** (Phase 5): Production Docker deployment
**Increment 4** (Phase 6): Configurable costing
**Increment 5** (Phase 7): Documentation and polish

---

## Validation Checkpoints

**Checkpoint 1** (After Phase 2):
- [ ] docker-compose.yml created and valid
- [ ] .env.example template complete

**Checkpoint 2** (After Phase 3):
- [ ] odoo_manager.py implements all 4 methods
- [ ] authenticate() returns valid uid
- [ ] create_journal_entry() creates entry in Odoo

**Checkpoint 3** (After Phase 4):
- [ ] .env file exists and is in .gitignore
- [ ] odoo_manager.py loads credentials from env

**Checkpoint 4** (After Phase 5):
- [ ] Docker containers running and healthy
- [ ] Odoo database created
- [ ] Invoicing module installed

**Checkpoint 5** (After Phase 6):
- [ ] Base cost is configurable via .env
- [ ] Changing cost updates journal entry amounts

**Checkpoint 6** (After Phase 7):
- [ ] README.md updated with complete setup instructions
- [ ] All commands tested and working

---

**Next Command**: `/sp.implement` - Begin implementation following task order
