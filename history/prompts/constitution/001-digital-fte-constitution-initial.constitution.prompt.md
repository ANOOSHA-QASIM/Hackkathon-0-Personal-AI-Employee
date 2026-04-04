---
id: 001
title: digital-fte-constitution-initial
stage: constitution
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: none
branch: main
user: Faiz
command: /sp.constitution
labels: ["constitution", "governance", "initial-setup"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

/sp.constitution {
  "project_name": "Digital-FTE-2026",
  "purpose": "Autonomous Personal/Business AI Employee using Qwen Code + Obsidian.",
  "folder_structure": {
    "root": "E:/hackathon_0_digital_fte/AI_Employee_vault",
    "phases": ["/phase-1-foundation", "/phase-2-functional", "/phase-3-autonomous", "/phase-4-platinum"],
    "vault_core": ["/Inbox", "/Needs_Action", "/In_Progress", "/Approved", "/Rejected", "/Done", "/Accounting", "/Briefings", "/Logs"]
  },
  "rules": [
    "BRONZE-SPECIFIC: Manual file drops enter via /Inbox. Watcher detects and moves to /Needs_Action with metadata.",
    "SILVER-EVOLUTION: Automated Watchers (Gmail/WhatsApp) must write directly to /Needs_Action following the .md metadata schema.",
    "CLAIM-BY-MOVE: Agent must move tasks from /Needs_Action to /In_Progress to prevent double-work.",
    "HITL MANDATORY: All external actions (Payments/Emails/Posts) require human move to /Approved before execution.",
    "STRICT PHASE LOCK: Phase X must be 'Closed' before Phase Y starts.",
    "AUDIT LOGGING: All actions recorded in /Logs/YYYY-MM-DD.json.",
    "MINIMALISM: Design and branding tasks must follow 'dark theme, clean typography, no human icons'."
  ],
  "phases": [
    {
      "id": 1,
      "name": "Bronze: Foundation",
      "goal": "Setup Dashboard, Handbook, and local FileSystem Watcher."
    },
    {
      "id": 2,
      "name": "Silver: Functional Assistant",
      "goal": "Activate Gmail/WhatsApp/LinkedIn Watchers and HITL actions."
    },
    {
      "id": 3,
      "name": "Gold: Autonomous Employee",
      "goal": "Odoo Accounting, Business Audit, and Ralph Wiggum loops."
    },
    {
      "id": 4,
      "name": "Platinum: Executive Agent",
      "goal": "Cloud-Local sync, 24/7 triage, and domain specialization."
    }
  ]
}

## Response snapshot

Created Digital-FTE-2026 Constitution v1.0.0 with 7 core principles:
1. Inbox-First Data Entry - Manual files enter via /Inbox, Watcher moves to /Needs_Action
2. Needs_Action Schema Compliance - YAML frontmatter mandatory for agent parsing
3. Claim-By-Move Protocol - Atomic file moves prevent double-work
4. HITL Mandatory - External actions require /Approved before execution
5. Strict Phase Lock - Sequential gating, no parallel phases
6. Audit Logging - Daily JSON logs with SHA-256 sealing
7. Minimalist Design - Dark theme, clean typography, no human icons

Added folder structure documentation, phase-gated development criteria (Bronze→Silver→Gold→Platinum), operational workflow (task lifecycle, agent/human responsibilities), and governance rules (amendment process, versioning policy, compliance review).

## Outcome

- ✅ Impact: Constitution v1.0.0 ratified with 7 principles, 4 phases, governance framework
- 🧪 Tests: N/A (constitution document)
- 📁 Files: .specify/memory/constitution.md created
- 🔁 Next prompts: /sp.specify for Phase 1 Bronze features
- 🧠 Reflection: Template had 6 placeholder principles; user provided 7 rules → expanded to 7 principles

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results: N/A
- Prompt variant: Initial constitution creation
- Next experiment: Implement Phase 1 Bronze features per constitution
