---
id: 006
title: phase-2-functional-spec-creation
stage: spec
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-2-functional
branch: 002-phase-2-functional
user: Faiz
command: /sp.specify
labels: ["spec", "phase-2", "functional", "gmail", "linkedin", "hitl"]
links:
  spec: specs/002-phase-2-functional/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-phase-2-functional/spec.md
  - specs/002-phase-2-functional/checklists/requirements.md
tests:
  - N/A (specification phase)
---

## Prompt

/sp.specify { "phase": "phase-2-functional", "objective": "Activate external communication 'Senses' and LinkedIn posting capability.", "scope": [ "Connect Gmail MCP to monitor 'Unread' emails and create .md alerts in /Needs_Action.", "Implement LinkedIn Post Workflow: AI drafts content in /In_Progress, User moves to /Approved, AI posts via Playwright MCP.", "Develop 'Communication_Triage.py' to categorize incoming Gmail/LinkedIn messages by priority (High/Low).", "Define metadata schema for social media posts (Platform, Content, Media_Path, Scheduled_Time)." ], "constraints": [ "STRICT HITL: No LinkedIn post can be published without being moved to /Approved folder.", "Minimalist Design: All image-based posts must follow the dark-theme/clean typography rule.", "Gmail MCP must use the credentials.json path defined in Phase 1." ], "exit_criteria": "Successful test of an email alert appearing in /Needs_Action and a LinkedIn post successfully drafted in /In_Progress." }

## Response snapshot

Created feature specification for Phase 2 Functional with:

**4 User Stories**:
1. Gmail Email Alerts (P1) - Unread emails → /Needs_Action alerts within 5 minutes
2. LinkedIn Post Workflow with HITL (P1) - Draft in /In_Progress, approve in /Approved, publish
3. Communication Triage by Priority (P2) - Auto-categorize messages (High/Low priority)
4. Social Media Metadata Schema (P2) - Structured metadata for posts (platform, content, media_path, scheduled_time)

**15 Functional Requirements** covering: Gmail API integration, email monitoring (5-min intervals), alert metadata, priority categorization, LinkedIn posting, HITL enforcement, minimalist design, duplicate prevention, rate limit handling, audit logging, post scheduling, credential expiry handling.

**10 Success Criteria** including: Email alerts within 5 minutes (95%), zero duplicate alerts, 100% HITL compliance, high-priority accuracy 90%, scheduled posts within 2 minutes, zero invalid metadata posts, 50+ emails/day auto-triaged, 100% minimalist design compliance, credential expiry alert within 1 minute, rate limits handled gracefully.

**Key Entities**: Email Alert, Social Media Post, Communication Triage, HITL Gate, Credential Store

**Edge Cases**: Gmail API credential expiry, LinkedIn rate limits, invalid metadata, duplicate emails, post revision workflow

Validation: All checklist items passed, no NEEDS CLARIFICATION markers, spec ready for /sp.plan

## Outcome

- ✅ Impact: Specification complete for Phase 2 Functional (Gmail alerts, LinkedIn posting with HITL, communication triage, metadata schema)
- 🧪 Tests: N/A (specification phase - tests will be created in /sp.tasks)
- 📁 Files: specs/002-phase-2-functional/spec.md, checklists/requirements.md
- 🔁 Next prompts: /sp.plan for technical implementation plan
- 🧠 Reflection: No clarifications needed - all requirements derived from input with reasonable defaults per Constitution

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results: Specification quality checklist - all items PASS
- Prompt variant: Initial spec creation for phase-2-functional
- Next experiment: Proceed to /sp.plan for technical architecture
