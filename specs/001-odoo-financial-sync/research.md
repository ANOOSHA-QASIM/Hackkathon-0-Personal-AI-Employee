# Research & Technology Decisions: Odoo Financial Integration

**Feature**: Dockerized Odoo AI Accountant
**Branch**: `001-odoo-financial-sync`
**Date**: 2026-03-28

---

## Decision: Odoo Authentication Method

**What was chosen**: XML-RPC with UID authentication

**Rationale**:
- Odoo 17.0 supports XML-RPC out of the box (Community Edition)
- Python stdlib includes `xmlrpc.client` (no extra dependencies required)
- Well-documented Odoo API pattern with extensive community examples
- Supports all required operations (create accounting entries, query chart of accounts)
- Simple authentication flow: common_auth → returns uid for subsequent calls
- Works with Odoo Community Edition (no Enterprise license required)

**Alternatives considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| JSON-RPC | Modern protocol, slightly faster | Requires additional setup, less documented for accounting module | XML-RPC has better Community support |
| Odoo ORM via SSH | Full ORM access, familiar API | Overkill for simple expense logging, security complexity | Unnecessary complexity for our use case |
| Odoo Studio custom API | Visual builder, no code | Requires Odoo Enterprise (paid license) | We use Community Edition |
| Webhook-based integration | Event-driven, real-time | Requires Enterprise, complex setup | XML-RPC polling is sufficient for our needs |

**Source**: 
- Odoo 17.0 Developer Documentation - XML-RPC API
- Odoo Community Forum - Authentication best practices
- GitHub: odoo/odoo repository - XML-RPC examples

---

## Decision: Docker Compose Structure

**What was chosen**: Single compose file with Odoo + PostgreSQL services

**Rationale**:
- Simplest deployment for single-server setup (one command: `docker-compose up -d`)
- Volume persistence ensures data survives container restarts/removal
- Port 8069 exposed for local browser access and Python API calls
- Official Odoo Docker image includes all dependencies (no manual installation)
- PostgreSQL 15 is the recommended database for Odoo 17.0
- Health checks built into official images ensure reliability

**Alternatives considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Separate compose files per service | Fine-grained control | Unnecessary complexity for 2 services | Single file is simpler to manage |
| Kubernetes | Scalability, orchestration | Overkill for single-server deployment | We're not running a cluster |
| Manual installation | Full control, no Docker | Loses portability, harder to reproduce | Docker provides consistency across environments |
| Odoo.sh (Odoo hosting) | Managed service, auto-scaling | Monthly cost, less control | Self-hosted is free and sufficient for our scale |

**Source**:
- Official Odoo Docker documentation
- Docker Compose best practices
- Odoo Deployment Guide

---

## Decision: Expense Logging Pattern

**What was chosen**: Create `account.move` entries directly via XML-RPC

**Rationale**:
- `account.move` is the standard Odoo model for journal entries (works with Community)
- Automatically appears in accounting reports and financial statements
- Supports reconciliation with bank statements later
- Simple XML-RPC call: `create()` method on `account.move` model
- No custom module development required
- Entries are immediately visible in Odoo UI

**Alternatives considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Create `account.payment` entries | More structured for payments | Requires vendor setup, more complex | We're logging expenses, not making payments |
| Use Odoo webhooks | Event-driven, automatic | Requires Odoo Enterprise | We use Community Edition |
| CSV import | Simple, no API needed | Not real-time, loses audit trail, manual process | We need automatic, real-time logging |
| Custom Odoo module | Full control, tailored logic | Requires development, testing, maintenance | Standard `account.move` meets our needs |

**Source**:
- Odoo Accounting Developer Guide
- Odoo 17.0 Models Reference - account.move
- GitHub: Odoo Community modules - expense logging examples

---

## Decision: Error Resilience Pattern

**What was chosen**: Graceful degradation with warning logs

**Rationale**:
- Social media posting MUST continue even if Odoo is unavailable (Constitution Principle IV)
- Warning logs provide visibility into sync failures
- Retry logic with exponential backoff prevents overwhelming Odoo during outages
- Simple pattern: try/except around Odoo calls, log warning on failure, continue
- No complex circuit breaker needed for single-service integration

**Alternatives considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Circuit breaker pattern | Prevents repeated failures | Over-engineering for single service | Simple try/except is sufficient |
| Queue-based retry | Guaranteed eventual consistency | Adds complexity (queue, worker) | Not needed for expense logging (can be manual later) |
| Fail-fast with exception | Immediate feedback | Stops social posting (violates Constitution) | Cannot block posting workflow |
| Synchronous blocking wait | Ensures consistency | Blocks posting, poor UX | Asynchronous logging is better |

**Source**:
- Constitution Principle IV: HITL Mandatory for External Actions
- Error handling best practices for microservices
- Odoo API timeout recommendations

---

## Decision: Chart of Accounts Configuration

**What was chosen**: Configurable account code via .env (default: 500000)

**Rationale**:
- Different businesses have different chart of accounts structures
- Making account code configurable allows flexibility without code changes
- Default value (500000) follows standard accounting numbering (5xxxx = Expense accounts)
- Stored in .env alongside other Odoo configuration
- Easy to change without code deployment

**Alternatives considered**:

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Hardcoded account code | Simple, no configuration | Inflexible, breaks for different businesses | Configurability is essential |
| Auto-detect by name | No manual config | Name variations across locales/industries | Account code is more reliable |
| Fixed "Marketing Expense" account | Standardized | May conflict with existing accounts | Flexibility is better |

**Source**:
- Standard Chart of Accounts numbering conventions
- Odoo Configuration best practices
- Small business accounting standards

---

## Technology Stack Summary

| Component | Technology | Version | Source |
|-----------|------------|---------|--------|
| Container Orchestration | Docker Compose | Latest | docker.com |
| ERP System | Odoo Community | 17.0 | odoo.com |
| Database | PostgreSQL | 15 | postgresql.org |
| API Protocol | XML-RPC | Standard | w3.org |
| Python Library | xmlrpc.client | Stdlib | docs.python.org |
| Environment Config | python-dotenv | Latest | pypi.org |
| Accounting Model | account.move | Odoo Standard | Odoo 17.0 docs |

---

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Social Orchestrator                       │
│  (src/skills/social_orchestrator.py)                         │
│                                                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │  Facebook   │  │  Instagram  │  │   Twitter   │          │
│  │   Poster    │  │   Poster    │  │   Poster    │          │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘          │
│         │                │                │                   │
│         └────────────────┴────────────────┘                   │
│                          │                                    │
│                    (after post)                               │
│                          │                                    │
│                          ▼                                    │
│              ┌───────────────────────┐                        │
│              │    OdooManager Skill  │                        │
│              │  (src/skills/odoo_    │                        │
│              │   manager.py)         │                        │
│              └───────────┬───────────┘                        │
└──────────────────────────┼────────────────────────────────────┘
                           │
                           │ XML-RPC
                           │ (account.move.create)
                           │
                           ▼
              ┌───────────────────────────┐
              │   Odoo 17.0 (Docker)      │
              │  Port: 8069               │
              │                           │
              │  ┌─────────────────────┐  │
              │  │  PostgreSQL 15      │  │
              │  │  (account_move tbl) │  │
              │  └─────────────────────┘  │
              └───────────────────────────┘
```

---

## Next Steps

1. **Infrastructure**: Create docker-compose.yml
2. **Skill Development**: Implement odoo_manager.py
3. **Integration**: Hook into social_orchestrator.py
4. **Testing**: Verify end-to-end flow (post → Odoo entry)
5. **Documentation**: Update README with setup instructions

**Ready for**: `/sp.tasks` - Task breakdown for implementation
