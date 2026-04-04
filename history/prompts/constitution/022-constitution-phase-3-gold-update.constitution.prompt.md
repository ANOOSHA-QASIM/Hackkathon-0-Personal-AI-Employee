---
id: 022
title: constitution-phase-3-gold-update
stage: constitution
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: constitution
branch: main
user: Faiz
command: /sp.constitution
labels: ["constitution", "phase-3", "gold", "autonomous", "odoo", "social-media", "ralph-wiggum"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md (updated v1.0.0 → v2.0.0)
tests:
  - N/A (constitution update)
---

## Prompt

/sp.constitution { "action": "update", "phase": "Phase 3: Gold (Autonomous Employee)", "updates": [ "1. INTEGRATION: Add Odoo Community (Local) via JSON-RPC MCP server for business accounting.", "2. SOCIAL: Add Facebook, Instagram, and Twitter (X) as core Agent Skills for automated posting and summary generation.", "3. REASONING: Implement 'Ralph Wiggum' loops for autonomous multi-step task completion and error recovery.", "4. AUDIT: Weekly Business and Accounting Audit with CEO Briefing generation in /Briefings/ folder.", "5. ARCHITECTURE: All AI functionality must be implemented as modular 'Agent Skills' (src/skills/)." ] }

## Response snapshot

Updated Constitution to v2.0.0 with Phase 3: Gold (Autonomous Employee) features:

**New Principles Added**:
- VII. Weekly Business Audit - Weekly CEO Briefings in /Briefings/
- VIII. Modular Agent Skills Architecture - All AI as modular skills in src/skills/
- IX. Ralph Wiggum Autonomous Reasoning - Multi-step task completion with error recovery
- X. Minimalist Design (renumbered from VII)

**Updated Principles**:
- II. Needs_Action Schema - Added Facebook, Instagram, Twitter to watchers
- IV. HITL Mandatory - Added Odoo transactions to external actions

**New Sections**:
- Odoo Community Integration - JSON-RPC MCP for accounting
- Social Media Platforms - Facebook, Instagram, Twitter (X) as core platforms

**Phase Updates**:
- Phase 1: Status ✅ CLOSED
- Phase 2: Status ✅ CLOSED
- Phase 3: Status 🔄 IN PROGRESS (added detailed exit criteria)
- Phase 4: Status ⏳ PENDING

**Sync Impact Report**:
- Version: 1.0.0 → 2.0.0 (MAJOR bump - new principles added)
- Templates: All compatible (Constitution Check sections verified)
- Follow-up TODOs:
  - TODO(AGENT_SKILLS_DOC): Document modular skills architecture
  - TODO(RALPH_WIGGUM_SPEC): Create specification for reasoning loops
  - TODO(ODOO_MCP_CONFIG): Document Odoo JSON-RPC configuration

## Outcome

- ✅ Impact: Constitution now defines Phase 3: Gold with Odoo, social media, Ralph Wiggum
- 🧪 Tests: N/A (constitution update)
- 📁 Files: .specify/memory/constitution.md updated v1.0.0 → v2.0.0
- 🔁 Next prompts: /sp.specify for Phase 3 features
- 🧠 Reflection: MAJOR version bump justified by 3 new principles + new sections

## Evaluation notes (flywheel)

- Failure modes observed: None (constitution update successful)
- Graders run and results: N/A
- Prompt variant: Constitution update for Phase 3
- Next experiment: Create specifications for Odoo integration, Ralph Wiggum loops
