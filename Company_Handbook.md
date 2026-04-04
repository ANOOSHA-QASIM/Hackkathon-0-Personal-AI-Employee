# Company Handbook

**Version**: 1.0.0  
**Effective Date**: 2026-03-28  
**Phase**: 1 (Foundation)

---

## Purpose

This handbook defines the "Rules of Engagement" for the Digital FTE autonomous employee system. All AI agents MUST follow these rules when processing tasks, making decisions, and communicating.

---

## Core Rules of Engagement

### RULE-001: HITL for Payments (Human-in-the-Loop)

**Category**: Escalation

**Description**: All payments MUST follow this escalation matrix:

| Amount | Action |
|--------|--------|
| ≤ $100 | Process autonomously, log to audit |
| $101 - $500 | Process autonomously, flag in daily briefing |
| $501 - $5,000 | Move to `/Approved` for human review |
| > $5,000 | Move to `/Approved` with justification memo |

**Examples**:
- Invoice $75 → Process and log
- Invoice $350 → Process, flag in briefing
- Invoice $2,500 → Move to `/Approved` with invoice attached

---

### RULE-002: Audit Logging Mandatory

**Category**: Workflow

**Description**: All agent actions MUST be logged to `/Logs/YYYY-MM-DD.json` with:

- Timestamp (ISO 8601)
- Action type (file_detected, metadata_created, file_moved, error)
- Agent identifier
- File path affected
- Status (pending, completed, blocked, error)

**Daily Sealing**: At end-of-day, logs MUST be sealed with SHA-256 hash.

---

### RULE-003: Minimalist Design

**Category**: Communication

**Description**: All public-facing content and UI MUST follow minimalist design principles:

- **Theme**: Dark mode preferred
- **Typography**: Clean, readable fonts (Arial, Helvetica, Inter)
- **Colors**: Monochrome + single accent color
- **Images**: No human icons/avatars; use abstract graphics or logos
- **Logo**: Use company logo consistently

---

### RULE-004: Privacy First

**Category**: Security

**Description**: The following data types MUST be protected:

| Data Type | Handling |
|-----------|----------|
| **PII** (names, emails, phones) | Encrypt at rest, minimize logging |
| **Financial** (bank accounts, invoices) | Access logging, HITL for > $500 |
| **Credentials** (passwords, API keys) | Never log, store in `.env` only |
| **Health information** | Encrypt, restrict access |

**Credentials MUST NEVER be**:
- Stored in Markdown files
- Logged to audit files
- Sent via email or chat
- Displayed in Dashboard or Handbook

---

### RULE-005: Claim-by-Move Protocol

**Category**: Workflow

**Description**: Agents MUST claim tasks by moving them from `/Needs_Action` to `/In_Progress/{agent-name}/`. This prevents double-work.

**Process**:
1. Scan `/Needs_Action` for unclaimed tasks
2. Move task to `/In_Progress/{your-agent-name}/`
3. Update frontmatter: `assigned_to: {your-agent-name}`, `claimed_at: {timestamp}`
4. Begin processing

**Violation**: Processing a task without claiming it first is prohibited.

---

## Decision Matrix

### When in Doubt, Ask This:

```
1. Is this a payment or external action?
   → Yes: Check RULE-001 (HITL for Payments)
   
2. Am I unsure about the correct action?
   → Yes: Move to `/Approved` with question for human
   
3. Did an error occur?
   → Yes: Log to audit, escalate if system-critical
   
4. Is this task time-sensitive?
   → Yes: Prioritize as urgent, process within 1 hour
   
5. Does this involve sensitive data?
   → Yes: Check RULE-004 (Privacy First)
```

---

## Quick Reference

| Rule ID | Category | Summary |
|---------|----------|---------|
| RULE-001 | Escalation | HITL for payments (>$500 requires approval) |
| RULE-002 | Workflow | Audit logging mandatory for all actions |
| RULE-003 | Communication | Minimalist design (dark theme, clean typography) |
| RULE-004 | Security | Privacy first (credentials never in Markdown) |
| RULE-005 | Workflow | Claim-by-move (prevent double-work) |

---

## Amendment Process

This handbook MAY be amended by:

1. **Proposal**: Document proposed change with rationale
2. **Review**: Assess impact on existing rules and workflows
3. **Approval**: Human approval required
4. **Documentation**: Update handbook with version increment

**Version History**:
- v1.0.0 (2026-03-28): Initial ratification with 5 core rules
