---
id: 023
title: phase-3-social-media-suite-spec
stage: spec
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-3-social-media-suite
branch: 003-phase-3-social-media-suite
user: Faiz
command: /sp.specify
labels: ["spec", "phase-3", "social-media", "facebook", "instagram", "twitter", "gold-tier"]
links:
  spec: specs/003-phase-3-social-media-suite/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-phase-3-social-media-suite/spec.md
  - specs/003-phase-3-social-media-suite/checklists/requirements.md
tests:
  - N/A (specification phase)
---

## Prompt

/sp.specify { "goal": "Implement Gold Tier Social Media Suite (FB, IG, X)", "requirements": [ "1. SKILL - META: Create 'src/skills/meta_poster.py' for Facebook and Instagram posting using Playwright (persistent session: .browser_data/meta).", "2. SKILL - TWITTER: Create 'src/skills/twitter_poster.py' for X (Twitter) posting. Support single tweets and auto-threading for long content.", "3. CROSS-PLATFORM ORCHESTRATOR: Update 'src/linkedin/linkedin_poster.py' (or create a new master_poster.py) that triggers ALL 4 platforms (LinkedIn, FB, IG, X) when a file enters '/Approved/Social'.", "4. IMAGE HANDLING: Ensure X and Instagram correctly pick up image attachments from the metadata 'media_path'.", "5. RALPH WIGGUM LOGIC: If one platform fails (e.g., Twitter API limit), the agent must log the error, wait 15 mins, and retry automatically without human intervention." ], "context": "Gold Tier Requirement. Expanding from Silver (LinkedIn) to a full autonomous social media presence." }

## Response snapshot

Created feature specification for Phase 3 Social Media Suite with:

**4 User Stories**:
1. Cross-Platform Social Posting (P1) - Single post → all 4 platforms
2. Meta Platform Integration (P1) - Facebook/Instagram with persistent sessions
3. Twitter (X) Integration (P2) - Single tweets + auto-threading
4. Ralph Wiggum Error Recovery (P2) - Autonomous retry with escalation

**14 Functional Requirements** covering:
- Meta Poster skill (Facebook + Instagram)
- Twitter Poster skill with auto-threading
- Cross-Platform Orchestrator (4 platforms)
- Image handling from media_path
- Ralph Wiggum error recovery (15-min retry, max 3 attempts)
- Status tracking per platform
- Metadata updates with platform URLs
- Success/failure file management

**8 Success Criteria** including:
- 95% posts published to all 4 platforms within 10 minutes
- Auto-threading 100% accurate for Twitter
- Image upload 95% success rate
- Ralph Wiggum 90% recovery without human intervention
- Persistent sessions reduce auth time from 2min to <10sec

**Key Entities**: Social Media Post, Platform Skill, Cross-Platform Orchestrator, Ralph Wiggum Loop, Persistent Session

**Edge Cases**: Missing images, content restrictions, corrupted sessions, long Instagram posts, orchestrator crash recovery

Validation: All checklist items passed, no NEEDS CLARIFICATION markers, spec ready for /sp.plan

## Outcome

- ✅ Impact: Specification complete for Phase 3 Social Media Suite (4 platforms, Ralph Wiggum recovery)
- 🧪 Tests: N/A (specification phase - tests will be created in /sp.tasks)
- 📁 Files: specs/003-phase-3-social-media-suite/spec.md, checklists/requirements.md
- 🔁 Next prompts: /sp.plan for technical implementation plan
- 🧠 Reflection: No clarifications needed - all requirements derived from input with reasonable defaults

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results: Specification quality checklist - all items PASS
- Prompt variant: Initial spec creation for phase-3-social-media-suite
- Next experiment: Proceed to /sp.plan for technical architecture
