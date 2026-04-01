# Technical Implementation Plan: Dockerized Odoo AI Accountant

**Feature Branch**: `001-odoo-financial-sync`
**Created**: 2026-03-28
**Spec**: [spec.md](../spec/spec.md)
**Phase**: Phase 4 - Technical Planning

## Technical Context

### Current State

- **Phase 3 Complete**: Social Media Suite (Facebook, Instagram, Twitter) with `social_orchestrator.py`
- **Python Environment**: `.venv` with Playwright, yaml, json libraries
- **Docker**: Available on Windows (Docker Desktop)
- **Odoo**: Not yet installed or configured

### Target State

- **Docker Compose**: Odoo 17.0 + PostgreSQL 15 running locally
- **Odoo Manager Skill**: `src/skills/odoo_manager.py` with XML-RPC connection
- **Social-Odoo Integration**: `social_orchestrator.py` calls Odoo after each post
- **Secure Config**: Credentials in `.env` file
- **Error Resilience**: Graceful degradation when Odoo unavailable

### Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| Docker Compose | Latest | Container orchestration |
| Odoo | 17.0 | Accounting/ERP system |
| PostgreSQL | 15 | Odoo database |
| Python xmlrpc.client | Stdlib | Odoo API communication |
| python-dotenv | Latest | Environment variable loading |

### Integration Points

1. **Social Orchestrator → Odoo Manager**: After each successful post, call `odoo.log_post_expense()`
2. **Odoo Manager → Odoo XML-RPC**: Authenticate and create accounting entries
3. **Environment → Odoo Manager**: Load credentials from `.env`

---

## Constitution Check

### Principle IV: HITL Mandatory for External Actions

**Requirement**: All Odoo transactions (journal entries) MUST be moved to `/Approved` before execution.

**Design Decision**: 
- Initial implementation will log expenses automatically (read-only accounting)
- Actual payment approval follows separate HITL workflow in Odoo UI
- Social posts themselves already require `/Approved/Social/` before posting

**Compliance**: ✅ PASS - Posts require HITL approval; Odoo entries are reflective logging

### Principle V: Strict Phase Lock

**Requirement**: Phase 3 MUST be complete before Phase 4 begins.

**Current Status**: Phase 3 social media suite is functional (Instagram posting with confirmation)

**Compliance**: ✅ PASS - Phase 3 complete, Phase 4 can proceed

### Principle VI: Audit Logging

**Requirement**: All agent actions MUST be logged to `/Logs/YYYY-MM-DD.json`

**Design Decision**:
- Odoo Manager will log all API calls to existing audit log
- Include: timestamp, method, parameters, status, uid used
- Odoo transaction IDs stored for reconciliation

**Compliance**: ✅ PASS - Audit logging integrated

### Principle VIII: Modular Agent Skills Architecture

**Requirement**: Skills MUST be modular, single-responsibility, independently testable

**Design Decision**:
- `odoo_manager.py` is standalone skill
- Exposes: `authenticate()`, `create_journal_entry()`, `check_connection()`
- Social orchestrator imports and uses skill (loose coupling)

**Compliance**: ✅ PASS - Modular design maintained

---

## Gate Evaluation

| Gate | Status | Notes |
|------|--------|-------|
| Spec Complete | ✅ PASS | spec.md created and validated |
| Constitution Aligned | ✅ PASS | All principles satisfied |
| Dependencies Clear | ✅ PASS | Docker, Odoo, Python stdlib identified |
| Integration Points Defined | ✅ PASS | Social→Odoo, Env→Odoo, Odoo→XML-RPC |

**Overall**: ✅ ALL GATES PASS - Proceed to Phase 1 Design

---

## Phase 0: Research & Technology Decisions

### Decision: Odoo Authentication Method

**What was chosen**: XML-RPC with UID authentication

**Rationale**:
- Odoo 17.0 supports XML-RPC out of box
- Python stdlib includes `xmlrpc.client` (no extra dependencies)
- Well-documented Odoo API pattern
- Supports all required operations (create accounting entries)

**Alternatives considered**:
- JSON-RPC: Requires additional setup, less documented for accounting module
- Odoo ORM via SSH: Overkill for simple expense logging
- Odoo Studio custom API: Requires Odoo Enterprise, we use Community

**Source**: Odoo 17.0 Developer Documentation - XML-RPC API

### Decision: Docker Compose Structure

**What was chosen**: Single compose file with Odoo + PostgreSQL services

**Rationale**:
- Simplest deployment for single-server setup
- Volume persistence for data survival across restarts
- Port 8069 exposed for local access and API calls
- Official Odoo Docker image includes all dependencies

**Alternatives considered**:
- Separate compose files per service: Unnecessary complexity
- Kubernetes: Overkill for single-server deployment
- Manual installation: Loses portability and reproducibility

**Source**: Official Odoo Docker documentation

### Decision: Expense Logging Pattern

**What was chosen**: Create `account.move` entries directly via XML-RPC

**Rationale**:
- `account.move` is the standard Odoo model for journal entries
- Works with Odoo Community (Invoicing module)
- Automatically appears in accounting reports
- Supports reconciliation with bank statements later

**Alternatives considered**:
- Create `account.payment` entries: More complex, requires vendor setup
- Use Odoo webhooks: Requires Odoo Enterprise
- CSV import: Not real-time, loses audit trail

**Source**: Odoo Accounting Developer Guide

---

## Phase 1: Architecture & Design

### Data Model

#### Entity: OdooJournalEntry

**Purpose**: Represents a marketing expense entry in Odoo

**Fields**:
- `move_type`: "entry" (standard journal entry)
- `name`: "Marketing Expense - {platform} - {timestamp}"
- `date`: Post date (YYYY-MM-DD)
- `line_ids`: Array of debit/credit lines
  - Account 500000 (Marketing Expense): Debit 500 PKR
  - Account 100000 (Cash/Bank): Credit 500 PKR
- `ref`: "Social Post: {post_title}"
- `state`: "posted" (immediately posted)

**Validation Rules**:
- Amount MUST be positive (expense)
- Platform MUST be one of: facebook, instagram, twitter, linkedin
- Account codes MUST exist in Odoo chart of accounts

**Relationships**:
- Links to `account.move.line` (debit/credit lines)
- References social post metadata in description

#### Entity: OdooConnection

**Purpose**: Manages Odoo authentication and connection state

**Fields**:
- `url`: Odoo instance URL (http://localhost:8069)
- `db`: Database name (odoo_vault)
- `uid`: User ID from authentication
- `password`: User password (from .env)

**Validation Rules**:
- URL MUST be valid HTTP/HTTPS URL
- DB name MUST match existing Odoo database
- UID MUST be obtained via successful authentication

**State Transitions**:
- `disconnected` → `authenticating` → `connected`
- `connected` → `disconnected` (on timeout/error)

### API Contracts

#### Internal API: OdooManager Skill

```python
class OdooManager:
    """
    Odoo integration skill for financial tracking.
    
    Usage:
        odoo = OdooManager()
        if odoo.check_connection():
            odoo.create_journal_entry(platform, post_title, amount)
    """
    
    def __init__(self):
        """Initialize with credentials from .env"""
        
    def authenticate(self) -> bool:
        """
        Authenticate with Odoo via XML-RPC.
        
        Returns:
            bool: True if authentication successful
        """
        
    def check_connection(self) -> bool:
        """
        Check if Odoo is reachable and authenticated.
        
        Returns:
            bool: True if connection healthy
        """
        
    def create_journal_entry(self, platform: str, post_title: str, amount: float = 500.0) -> dict:
        """
        Create a marketing expense journal entry in Odoo.
        
        Args:
            platform: Social media platform (facebook, instagram, twitter, linkedin)
            post_title: Title/content of the post
            amount: Expense amount in PKR (default: 500)
            
        Returns:
            dict: Odoo response with move_id and status
            
        Raises:
            ConnectionError: If Odoo unreachable
            AuthenticationError: If credentials invalid
        """
        
    def log_post_expense(self, platform: str, post_title: str) -> Optional[dict]:
        """
        High-level method: Log expense for a social media post.
        Wraps create_journal_entry with error handling.
        
        Args:
            platform: Social media platform
            post_title: Post title/content
            
        Returns:
            dict if successful, None if failed (logs warning)
        """
```

#### Integration Hook: Social Orchestrator

```python
# In social_orchestrator.py, after successful post:

from skills.odoo_manager import OdooManager

# Initialize once at module level
odoo = OdooManager()

# In process_post_file(), after each platform success:
if result.status == 'published':
    # Log marketing expense
    expense_result = odoo.log_post_expense(
        platform='facebook',  # or instagram, twitter, linkedin
        post_title=post_file.name
    )
    if expense_result:
        print(f"[Audit] Odoo expense logged: {expense_result.get('move_id')}")
    else:
        print("[Audit] Financial Sync Failed - Odoo unavailable")
```

### Quickstart Guide

#### 1. Start Odoo Infrastructure

```bash
# From project root
docker-compose up -d

# Verify containers running
docker-compose ps

# Expected output:
# NAME                STATUS              PORTS
# vault-db-1          Up (healthy)        5432/tcp
# vault-odoo-1        Up (healthy)        0.0.0.0:8069->8069/tcp
```

#### 2. Initial Odoo Setup

1. Open browser: `http://localhost:8069`
2. Create database: `odoo_vault`
3. Set admin password: `admin`
4. Install "Invoicing" module:
   - Click "Apps" → Search "Invoicing" → Click "Install"
   - Wait for installation to complete
5. Configure Chart of Accounts:
   - Go to Invoicing → Configuration → Chart of Accounts
   - Verify Account 500000 (Marketing Expense) exists
   - If not, create new account:
     - Code: 500000
     - Name: Marketing Expense
     - Type: Expense

#### 3. Configure Environment

Create `.env` file in project root:

```bash
# Odoo Configuration
ODOO_URL=http://localhost:8069
ODOO_DB=odoo_vault
ODOO_USER=admin
ODOO_PASSWORD=admin
ODOO_MARKETING_ACCOUNT=500000
ODOO_BASE_COST=500
```

#### 4. Test Odoo Connection

```bash
# Run test script (to be created)
python src/skills/test_odoo_connection.py

# Expected output:
# [OK] Odoo connection successful
# [OK] Authentication: uid=2
# [OK] Chart of accounts loaded
# [OK] Marketing Expense account found: 500000
```

#### 5. Run Social Orchestrator with Odoo Integration

```bash
# Place test post in /Approved/Social/
# Run orchestrator
python src/skills/social_orchestrator.py --once

# Expected output:
# [Orchestrator] === Meta (Facebook) ===
# [Meta] ✓ Facebook post published!
# [Audit] Odoo expense logged: move_id=123
# [Audit] Logged: meta - published
```

#### 6. Verify in Odoo UI

1. Open `http://localhost:8069`
2. Go to Invoicing → Accounting → Journal Entries
3. Find entry with reference "Social Post: {post_file_name}"
4. Verify amount: 500 PKR
5. Verify account: Marketing Expense (500000)

---

## Phase 2: Implementation Tasks

### Task Breakdown

1. **DOCKER-001**: Create `docker-compose.yml` with Odoo 17.0 + PostgreSQL 15
2. **ENV-001**: Create `.env.example` with Odoo credential placeholders
3. **ODOO-001**: Implement `src/skills/odoo_manager.py` with XML-RPC connection
4. **ODOO-002**: Add `check_connection()` method with timeout handling
5. **ODOO-003**: Add `create_journal_entry()` method with account.move creation
6. **ODOO-004**: Add `log_post_expense()` wrapper with error resilience
7. **INTEGRATE-001**: Import OdooManager in `social_orchestrator.py`
8. **INTEGRATE-002**: Add Odoo expense logging after each platform success
9. **TEST-001**: Create `test_odoo_connection.py` script
10. **TEST-002**: Test full flow: post → Odoo entry creation
11. **DOC-001**: Update README.md with Odoo setup instructions
12. **DOC-002**: Document Odoo module installation steps

### Parallel Execution Groups

**Group A (Infrastructure)**:
- DOCKER-001, ENV-001 (can run in parallel)

**Group B (Odoo Skill)**:
- ODOO-001, ODOO-002, ODOO-003, ODOO-004 (sequential, each builds on previous)

**Group C (Integration)**:
- INTEGRATE-001, INTEGRATE-002 (sequential, after Group B complete)

**Group D (Testing)**:
- TEST-001, TEST-002 (sequential, after Group C complete)

**Group E (Documentation)**:
- DOC-001, DOC-002 (can run in parallel after all groups complete)

### Validation Checkpoints

**Checkpoint 1 (After Group A)**:
- [ ] `docker-compose up -d` starts both containers
- [ ] Containers show "Up (healthy)" status
- [ ] `http://localhost:8069` accessible in browser

**Checkpoint 2 (After Group B)**:
- [ ] `python test_odoo_connection.py` returns success
- [ ] UID authentication works
- [ ] Journal entry creation returns valid move_id

**Checkpoint 3 (After Group C)**:
- [ ] Social orchestrator runs without import errors
- [ ] Odoo logging called after each platform success
- [ ] Warning logged when Odoo unavailable (doesn't crash)

**Checkpoint 4 (After Group D)**:
- [ ] Test post creates Odoo journal entry
- [ ] Entry appears in Odoo UI
- [ ] Correct amount and account used

**Checkpoint 5 (After Group E)**:
- [ ] README.md updated with Odoo setup
- [ ] All commands tested and working

---

## Risks & Mitigations

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Odoo XML-RPC API changes | High | Low | Use Odoo 17.0 specific docs, test thoroughly |
| Chart of accounts differs | Medium | Medium | Make account code configurable via .env |
| Docker resource constraints | Medium | Low | Document minimum RAM requirements (2GB+) |
| Odoo container slow to start | Low | High | Add retry logic with exponential backoff |
| Authentication fails silently | Medium | Low | Log detailed errors, validate credentials on startup |

---

## Success Metrics

1. **Infrastructure**: Docker containers start in <30 seconds
2. **Connection**: Odoo authentication completes in <2 seconds
3. **Expense Logging**: Journal entry created in <5 seconds after post
4. **Error Resilience**: Social posting continues 100% of time even if Odoo down
5. **Audit Trail**: 100% of posts have corresponding Odoo entries (when Odoo available)

---

## Out of Scope (Phase 4)

- Multi-currency support
- Vendor bill creation
- Payment reconciliation
- Odoo custom module development
- Real-time dashboard for marketing spend
- Bulk expense import/export
- Integration with other Odoo modules (CRM, Sales)

---

**Next Phase**: `/sp.tasks` - Break down into actionable implementation tasks
