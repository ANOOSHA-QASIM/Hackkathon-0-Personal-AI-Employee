---
id: 007
title: phase-2-functional-plan-creation
stage: plan
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-2-functional
branch: 002-phase-2-functional
user: Faiz
command: /sp.plan
labels: ["plan", "phase-2", "functional", "gmail", "linkedin", "hitl"]
links:
  spec: specs/002-phase-2-functional/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-phase-2-functional/plan.md
  - specs/002-phase-2-functional/research.md
  - specs/002-phase-2-functional/data-model.md
  - specs/002-phase-2-functional/quickstart.md
  - specs/002-phase-2-functional/contracts/email-alert-schema.yaml
  - specs/002-phase-2-functional/contracts/social-media-post-schema.yaml
tests:
  - N/A (planning phase)
---

## Prompt

/sp.plan { "phase": "phase-2-functional", "objective": "Implement Gmail monitoring and LinkedIn posting infrastructure.", "tasks": [ "Step 1: Test Playwright MCP connectivity to ensure LinkedIn login and navigation is possible.", "Step 2: Initialize Gmail MCP 'Watch' mode to scan for unread emails every 10 minutes.", "Step 3: Create 'Communication_Triage.py' to convert Gmail data into .md files in /Needs_Action.", "Step 4: Develop a 'LinkedIn_Draft_Generator' that creates post templates in /In_Progress.", "Step 5: Create an 'Execution_Script' that monitors /Approved and uses Playwright to post to LinkedIn.", "Step 6: Update Dashboard.md with a new 'Social & Email Feed' section." ], "verification": [ "Does a new Gmail email appear in /Needs_Action as a Markdown file?", "Does moving a LinkedIn draft to /Approved trigger the Playwright posting script?", "Is the minimalist design rule (dark theme/clean fonts) applied to post drafts?" ] }

## Response snapshot

Created implementation plan for Phase 2 Functional with:

**Technical Context**:
- Python 3.11+ with google-api-python-client, playwright, pyyaml
- File-based state management (Markdown + YAML frontmatter)
- Windows platform (E:/ drive)
- Gmail check every 5 minutes, LinkedIn publish within 10 minutes

**Constitution Check**: All 7 principles PASS
- I. Inbox-First: Gmail watcher → /Needs_Action
- II. Schema Compliance: Email alerts and posts have YAML frontmatter
- III. Claim-By-Move: LinkedIn agent claims via folder move
- IV. HITL Mandatory: LinkedIn posts require /Approved (enforced gate)
- V. Strict Phase Lock: Phase 1 complete (credentials.json exists)
- VI. Audit Logging: All Gmail/LinkedIn actions logged
- VII. Minimalist Design: Image posts enforce dark theme

**Phase 0 Research** (6 decisions):
1. google-api-python-client for Gmail (official, OAuth2)
2. Playwright for LinkedIn (no API approval needed)
3. Keyword + VIP rules for priority (simple, transparent)
4. Folder-based HITL gate (/Approved only)
5. credentials.json reuse (Phase 1 pattern)
6. processed_emails.json for deduplication

**Phase 1 Artifacts**:
- data-model.md: EmailAlert, SocialMediaPost, CommunicationTriage, HITLGate, ProcessedEmails
- contracts/: email-alert-schema.yaml, social-media-post-schema.yaml
- quickstart.md: Setup guide, Gmail auth, LinkedIn workflow, troubleshooting

**Source Structure**:
src/gmail/ (gmail_watcher.py, email_processor.py, triage.py)
src/linkedin/ (post_generator.py, linkedin_publisher.py, scheduler.py)
src/triage/ (communication_triage.py)
tests/contract/, tests/integration/, tests/unit/

**Next Steps**: Ready for /sp.tasks to break into implementation tasks

## Outcome

- ✅ Impact: Plan complete for Phase 2 Functional (Gmail monitoring, LinkedIn posting with HITL, communication triage)
- 🧪 Tests: N/A (planning phase - tests will be created in /sp.tasks)
- 📁 Files: 6 planning documents created in specs/002-phase-2-functional/
- 🔁 Next prompts: /sp.tasks for implementation task breakdown
- 🧠 Reflection: All research decisions align with Constitution; no clarifications needed

## Evaluation notes (flywheel)

- Failure modes observed: None (planning phase)
- Graders run and results: Constitution Check - all 7 principles PASS
- Prompt variant: Planning from spec + user tasks
- Next experiment: Proceed to /sp.tasks for task breakdown
