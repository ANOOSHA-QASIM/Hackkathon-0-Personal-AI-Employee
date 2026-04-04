<!--
SYNC IMPACT REPORT
==================
Version change: 1.0.0 → 2.0.0
Modified principles:
  - IV. HITL Mandatory (expanded to include Odoo transactions)
  - VII. Minimalist Design → VIII. (renumbered for new principles)
Added principles:
  - VIII. Modular Agent Skills Architecture
  - IX. Ralph Wiggum Autonomous Reasoning
Added sections:
  - Odoo Community Integration
  - Social Media Platforms (Facebook, Instagram, Twitter/X)
  - Weekly Business Audit & CEO Briefings
Removed sections: None
Templates requiring updates:
  - ✅ .specify/templates/plan-template.md - Constitution Check section compatible
  - ✅ .specify/templates/spec-template.md - No constitution-specific references
  - ✅ .specify/templates/tasks-template.md - Phase structure compatible
  - ⚠ .specify/templates/commands/*.md - May need Agent Skills documentation updates
Follow-up TODOs:
  - TODO(AGENT_SKILLS_DOC): Document modular skills architecture in skills/ folder
  - TODO(RALPH_WIGGUM_SPEC): Create specification for autonomous reasoning loops
  - TODO(ODOO_MCP_CONFIG): Document Odoo JSON-RPC MCP server configuration
-->

# Digital-FTE-2026 Constitution

Autonomous Personal/Business AI Employee using Qwen Code + Obsidian.

## Core Principles

### I. Inbox-First Data Entry

All manual file drops MUST enter via `/Inbox`. A Watcher process detects new files and moves them to `/Needs_Action` with appropriate metadata (timestamp, source, initial tags). No file bypasses the Inbox gateway.

**Rationale**: Single entry point ensures consistent processing, prevents orphaned files, and enables audit trail from moment of creation.

---

### II. Needs_Action Schema Compliance

All tasks in `/Needs_Action` MUST follow the Markdown metadata schema:
- YAML frontmatter with `status`, `created_at`, `source`, `tags`
- Clear task description in body
- Machine-readable format for agent parsing

Automated Watchers (Gmail, WhatsApp, LinkedIn, Facebook, Instagram, Twitter) MUST write directly to `/Needs_Action` following this schema.

**Rationale**: Structured metadata enables reliable agent automation, filtering, and reporting.

---

### III. Claim-By-Move Protocol

Agents MUST claim tasks by moving them from `/Needs_Action` to `/In_Progress/{agent-name}/`. This prevents double-work in multi-agent environments. A task without a lock file or agent assignment is unclaimed.

**Rationale**: File system moves are atomic operations that serve as distributed locks without requiring external coordination services.

---

### IV. HITL Mandatory for External Actions

All external actions (Payments, Emails, Public Posts, API calls with side effects, Odoo transactions) MUST be moved to `/Approved` by a human before execution. Agents MUST NOT execute actions from `/In_Progress` without explicit approval.

**Rationale**: Human-in-the-Loop gate prevents unauthorized financial transactions, communications, and ensures accountability for all external-facing operations.

---

### V. Strict Phase Lock

Development phases MUST follow sequential gating: Phase N MUST be marked 'Closed' before Phase N+1 begins. Parallel phase development is prohibited.

**Rationale**: Sequential phases ensure foundational stability, prevent technical debt accumulation, and enable clear progress tracking.

---

### VI. Audit Logging

All agent actions MUST be recorded in `/Logs/YYYY-MM-DD.json` with:
- Timestamp (ISO 8601)
- Action type
- Agent identifier
- File path affected
- Status (pending, completed, blocked, rejected)

Daily logs MUST be sealed with SHA-256 hash at end-of-day.

**Rationale**: Immutable audit trail enables compliance verification, debugging, and trust verification for autonomous operations.

---

### VII. Weekly Business Audit

A comprehensive business and accounting audit MUST be generated weekly in `/Briefings/` folder. The CEO Briefing MUST include:
- Revenue summary (from Odoo)
- Pending transactions requiring approval
- Social media engagement summary
- Critical alerts requiring human attention

**Rationale**: Regular executive summaries enable informed decision-making and maintain business oversight.

---

### VIII. Modular Agent Skills Architecture

All AI functionality MUST be implemented as modular 'Agent Skills' in `src/skills/`. Each skill MUST:
- Be self-contained and independently testable
- Follow the BaseSkill pattern with standard interface
- Declare dependencies and capabilities explicitly
- Log all actions to audit system

**Rationale**: Modular architecture enables scalability, maintainability, and skill reusability across agents.

---

### IX. Ralph Wiggum Autonomous Reasoning

Agents MUST implement autonomous multi-step task completion with error recovery through 'Ralph Wiggum' reasoning loops:
- Break complex tasks into atomic steps
- Validate each step before proceeding
- Retry failed steps with exponential backoff (max 3 attempts)
- Escalate to human if all retries exhausted

**Rationale**: Autonomous reasoning reduces human intervention for routine multi-step tasks while maintaining reliability.

---

### X. Minimalist Design

All UI, branding, and documentation tasks MUST follow: dark theme, clean typography, no human icons/avatars, minimal color palette (monochrome + single accent).

**Rationale**: Consistent visual language reduces cognitive load, maintains professional appearance, and aligns with automation-first philosophy.

---

## Folder Structure & Organization

### Root Structure

```
E:/hackathon_0_digital_fte/AI_Employee_vault/
├── /Inbox/              # Manual file drops (Watcher input)
├── /Needs_Action/       # Unclaimed tasks awaiting processing
├── /In_Progress/        # Claimed tasks by agent subfolder
├── /Approved/           # HITL-approved tasks awaiting execution
├── /Rejected/           # Human-rejected tasks with feedback
├── /Done/               # Completed tasks (archived by YYYY-MM/)
├── /Accounting/         # Financial records, invoices, reports
├── /Briefings/          # Daily/weekly summaries, executive reports
├── /Logs/               # Audit logs (YYYY-MM-DD.json)
└── /skills/             # Agent capability definitions (modular skills)
```

### Phase Folders

```
/phase-1-foundation/     # Bronze: Dashboard, Handbook, FileSystem Watcher
/phase-2-functional/     # Silver: Gmail/WhatsApp/LinkedIn/Facebook/Instagram/Twitter
/phase-3-autonomous/     # Gold: Odoo Accounting, Business Audit, Ralph Wiggum loops
/phase-4-platinum/       # Platinum: Cloud-Local sync, 24/7 triage, domain specialization
```

### In_Progress Subfolder Convention

```
/In_Progress/
├── /email-agent/
├── /accounting-agent/
├── /social-media-agent/
├── /audit-agent/
└── /ralph-wiggum-agent/
```

---

## Odoo Community Integration

### Architecture

Odoo Community (Local) MUST be integrated via JSON-RPC MCP server for:
- Bank transaction synchronization
- Invoice generation and tracking
- Payment reconciliation
- Revenue reporting

### Data Flow

1. Bank transactions → Odoo via JSON-RPC
2. Odoo → `/Accounting/Bank_Transactions.md` (daily sync)
3. Discrepancies → `/Needs_Action/` (for human review)
4. Weekly revenue → `/Briefings/CEO-Weekly-Briefing.md`

---

## Social Media Platforms

### Core Platforms

The following platforms are core Agent Skills for automated posting and summary generation:
- **LinkedIn**: Professional posts, engagement tracking
- **Facebook**: Business page posts, engagement summary
- **Instagram**: Visual posts (with minimalist design), stories
- **Twitter (X)**: Short updates, thread generation

### Posting Workflow

All social media posts MUST follow this workflow:
1. Draft created in `/In_Progress/social-media-agent/`
2. Human approval: Move to `/Approved/`
3. Agent posts via platform API or Playwright
4. Success: Move to `/Done/`
5. Engagement metrics logged to `/Briefings/Social-Media-Summary.md`

---

## Phase-Gated Development

### Phase 1: Bronze (Foundation)

**Goal**: Setup Dashboard, Handbook, and local FileSystem Watcher.

**Entry Criteria**: None (initial phase)

**Exit Criteria**:
- [x] Obsidian vault structure created
- [x] FileSystem Watcher detects `/Inbox` files
- [x] Files moved to `/Needs_Action` with metadata
- [x] Basic dashboard displays task counts

**Status**: ✅ CLOSED

---

### Phase 2: Silver (Functional Assistant)

**Goal**: Activate Gmail/WhatsApp/LinkedIn/Facebook/Instagram/Twitter Watchers and HITL actions.

**Entry Criteria**: Phase 1 marked 'Closed'

**Exit Criteria**:
- [x] Gmail Watcher operational (IMAP/API)
- [x] WhatsApp Watcher operational (Playwright)
- [x] LinkedIn Watcher operational (API/Playwright)
- [x] Facebook Watcher operational (Playwright)
- [x] Instagram Watcher operational (Playwright)
- [x] Twitter (X) Watcher operational (API/Playwright)
- [x] HITL approval workflow functional
- [x] All external actions require `/Approved` status

**Status**: ✅ CLOSED

---

### Phase 3: Gold (Autonomous Employee)

**Goal**: Odoo Accounting, Business Audit, and Ralph Wiggum loops.

**Entry Criteria**: Phase 2 marked 'Closed'

**Exit Criteria**:
- [ ] Odoo JSON-RPC integration complete
- [ ] Bank transaction auditing functional
- [ ] Weekly revenue reports generated
- [ ] Ralph Wiggum reasoning loops operational
- [ ] Daily audit summaries in `/Briefings/`
- [ ] Weekly CEO Briefings automated
- [ ] All Agent Skills modularized in `src/skills/`

**Status**: 🔄 IN PROGRESS

---

### Phase 4: Platinum (Executive Agent)

**Goal**: Cloud-Local sync, 24/7 triage, and domain specialization.

**Entry Criteria**: Phase 3 marked 'Closed'

**Exit Criteria**:
- [ ] Git/Syncthing sync between Cloud VM and Local
- [ ] Double-work prevention protocol active
- [ ] 24/7 triage with Sentinel Scripts
- [ ] Domain-specific agents deployed
- [ ] Full HITL compliance with audit sealing

**Status**: ⏳ PENDING

---

## Operational Workflow

### Task Lifecycle

1. **Creation**: Task created in `/Inbox` (manual) or `/Needs_Action` (automated)
2. **Claiming**: Agent moves task to `/In_Progress/{agent}/` and updates frontmatter
3. **Execution**: Agent processes task using modular Agent Skills, logs actions to `/Logs/`
4. **Ralph Wiggum Loop**: For multi-step tasks, validate each step, retry on failure
5. **HITL Check**: If sensitive action, move to `/Approved` and await human
6. **Completion**: Move to `/Done/{YYYY-MM}/` with `completed_at` timestamp
7. **Audit**: Daily log sealed with SHA-256 hash

### Agent Responsibilities

- Scan `/Needs_Action` for unclaimed tasks matching agent capabilities
- Claim tasks via move operation (atomic lock)
- Execute task per modular skill definition
- Implement Ralph Wiggum reasoning for multi-step tasks
- Log all actions with timestamps
- Respect HITL gates for sensitive operations
- Archive completed tasks with proper metadata
- Generate weekly summaries for `/Briefings/`

### Human Responsibilities

- Review `/Approved` tasks for HITL decisions
- Approve by moving to `/Approved/` (folder location = approval)
- Reject by moving to `/Rejected/` with comment
- Review weekly CEO Briefings in `/Briefings/`
- Seal audit logs (automated, manual verification optional)
- Update Agent Skills in `src/skills/` as needed

---

## Governance

### Amendment Process

This constitution supersedes all other practices. Amendments require:

1. **Proposal**: Document proposed change with rationale
2. **Review**: Assess impact on existing phases and agents
3. **Approval**: Human approval required for principle changes
4. **Migration**: Plan for transitioning existing tasks/files
5. **Documentation**: Update Sync Impact Report in constitution header

### Versioning Policy

Semantic versioning: `MAJOR.MINOR.PATCH`

- **MAJOR**: Backward-incompatible principle removals or redefinitions
- **MINOR**: New principles, sections, or material expansions
- **PATCH**: Clarifications, wording, typo fixes

### Compliance Review

- All agent implementations MUST verify constitution compliance
- Phase exit criteria MUST include principle adherence check
- Audit logs MUST be reviewed weekly for HITL compliance
- Constitution review scheduled quarterly
- Agent Skills MUST be tested against constitution principles

### Conflict Resolution

When principles conflict:
1. HITL Mandatory (IV) takes highest priority
2. Phase Lock (V) prevents unauthorized progression
3. Audit Logging (VI) ensures traceability
4. All other principles resolved by human decision

---

**Version**: 2.0.0 | **Ratified**: 2026-03-28 | **Last Amended**: 2026-03-28
