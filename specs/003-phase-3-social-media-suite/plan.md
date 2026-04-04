# Implementation Plan: Phase 3 Social Media Suite

**Branch**: `003-phase-3-social-media-suite` | **Date**: 2026-03-28 | **Spec**: [specs/003-phase-3-social-media-suite/spec.md](../spec.md)

**Input**: Implement Gold Tier Social Media Suite (Facebook, Instagram, Twitter/X) with modular Agent Skills, cross-platform orchestration, and Ralph Wiggum error recovery.

## Summary

Build Phase 3 Gold Tier social media automation expanding from Phase 2 (LinkedIn only) to full 4-platform suite (LinkedIn, Facebook, Instagram, Twitter/X). Implements modular Agent Skills architecture with Meta Poster (Facebook + Instagram), Twitter Poster with auto-threading, Cross-Platform Orchestrator for single-file multi-platform posting, and Ralph Wiggum autonomous error recovery with 15-minute retry cooldown. All components follow Constitution principles including modular skills, HITL gates, audit logging, and autonomous reasoning.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: 
- playwright (browser automation for all platforms)
- pyyaml (metadata parsing)
- python-dotenv (environment config)
- tweepy (Twitter API - optional fallback)
**Storage**: File-based (Markdown files with YAML frontmatter, browser sessions in `.browser_data/`)
**Testing**: pytest for unit tests, integration tests for each platform poster
**Target Platform**: Windows (E:/ drive local filesystem)
**Project Type**: Single Python service with modular skills architecture
**Performance Goals**: 
- 95% posts published to all 4 platforms within 10 minutes
- Auto-threading 100% accurate for Twitter
- Image upload 95% success rate
- Ralph Wiggum 90% recovery without human intervention
**Constraints**: 
- HITL mandatory for all social posts (Constitution Principle IV)
- Minimalist design for images (Constitution Principle X)
- Persistent sessions in `.browser_data/`
- All actions logged to /Logs/YYYY-MM-DD.json
**Scale/Scope**: 
- 4 platforms (LinkedIn, Facebook, Instagram, Twitter)
- 5-10 posts/week scheduling
- Auto-threading for Twitter (>280 chars)
- Image support for all platforms

## Constitution Check

**GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.**

| Principle | Compliance | Notes |
|-----------|------------|-------|
| I. Inbox-First Data Entry | ✅ PASS | Social posts enter via `/Approved/Social/` folder |
| II. Needs_Action Schema Compliance | ✅ PASS | All posts include YAML frontmatter with metadata |
| III. Claim-By-Move Protocol | ✅ PASS | Orchestrator claims posts by processing from `/Approved/Social/` |
| IV. HITL Mandatory for External Actions | ✅ PASS | All posts require move to `/Approved/Social/` before publishing |
| V. Strict Phase Lock | ✅ PASS | Phase 2 (LinkedIn) complete before Phase 3 starts |
| VI. Audit Logging | ✅ PASS | All platform actions logged to /Logs/YYYY-MM-DD.json |
| VII. Weekly Business Audit | ✅ PASS | Social media engagement included in weekly briefings |
| VIII. Modular Agent Skills Architecture | ✅ PASS | Meta Poster, Twitter Poster as modular skills in `src/skills/` |
| IX. Ralph Wiggum Autonomous Reasoning | ✅ PASS | Error recovery with retry logic and escalation |
| X. Minimalist Design | ✅ PASS | Image posts follow dark theme, clean typography |

**GATE RESULT**: ✅ PASS - All 10 constitution principles satisfied. Proceed to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/003-phase-3-social-media-suite/
├── plan.md              # This file
├── research.md          # Phase 0 output (platform API research)
├── data-model.md        # Phase 1 output (post schemas, session management)
├── quickstart.md        # Phase 1 output (setup guide)
└── contracts/           # Phase 1 output (post schemas)
    └── social-media-post-schema.yaml
```

### Source Code (repository root)

```text
src/
├── skills/
│   ├── __init__.py
│   ├── meta_poster.py       # Facebook + Instagram (Playwright)
│   ├── twitter_poster.py    # Twitter/X (Playwright + auto-threading)
│   └── base_poster.py       # Base class for all platform skills
├── orchestrator/
│   ├── __init__.py
│   └── social_dispatcher.py # Cross-platform orchestrator
├── utils/
│   ├── __init__.py
│   └── ralph_wiggum.py      # Error recovery logic
└── config/
    └── settings.py          # Environment configuration (extends Phase 1/2)

tests/
├── contract/
│   └── test_post_schema.py
├── integration/
│   ├── test_meta_poster.py
│   ├── test_twitter_poster.py
│   └── test_social_dispatcher.py
└── unit/
    ├── test_meta_poster.py
    ├── test_twitter_poster.py
    └── test_ralph_wiggum.py
```

**Structure Decision**: Modular skills architecture per Constitution Principle VIII. Each platform skill (`meta_poster.py`, `twitter_poster.py`) inherits from `base_poster.py` with standard interface. Orchestrator (`social_dispatcher.py`) coordinates all platforms. Ralph Wiggum logic centralized in `utils/ralph_wiggum.py` for reuse across skills.

## Complexity Tracking

No violations. All design decisions align with Constitution principles.

## Phase 0: Research & Technical Decisions

### Research Tasks Completed

1. **Meta (Facebook/Instagram) Automation Pattern**
   - Decision: Use Playwright for both platforms (unified Meta account)
   - Rationale: Consistent with Phase 2 LinkedIn approach, no API approval needed
   - Alternatives: Facebook Graph API (requires app review), Instagram Basic Display API (limited posting)

2. **Twitter (X) Automation Pattern**
   - Decision: Use Playwright for posting (primary), Tweepy as fallback
   - Rationale: Playwright consistent with other platforms, handles auth seamlessly
   - Alternatives: Twitter API v2 (requires developer account, rate limits)

3. **Auto-Threading Strategy**
   - Decision: Split at 280 characters, continue thread with "..." separator
   - Rationale: Standard Twitter threading pattern, preserves readability
   - Alternatives: Split at sentence boundaries (complex), manual thread markers

4. **Persistent Session Management**
   - Decision: Store in `.browser_data/meta` and `.browser_data/twitter`
   - Rationale: Consistent with Phase 2 LinkedIn (`.browser_data/linkedin`)
   - Alternatives: Cookie files (less secure), manual auth every time (friction)

5. **Ralph Wiggum Error Recovery**
   - Decision: 15-minute cooldown, max 3 retries, escalate to `/Needs_Action/`
   - Rationale: Balances persistence with eventual human oversight
   - Alternatives: Exponential backoff (complex), immediate retry (rate limit risk)

**All NEEDS CLARIFICATION markers resolved. Proceeding to Phase 1 design.**

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](data-model.md) for complete entity definitions:
- SocialMediaPost (content, media_path, platforms, status per platform)
- PlatformSkill (standard interface for all platforms)
- PostingResult (per-platform success/failure, URLs, timestamps)
- RalphWiggumState (retry count, last error, next retry time)

### API Contracts

See [contracts/](contracts/) for schema definitions:
- social-media-post-schema.yaml - YAML frontmatter for social posts

### Quickstart Guide

See [quickstart.md](quickstart.md) for setup and usage instructions.

### Agent Context Update

Modular skills architecture documented per Constitution Principle VIII.

## Constitution Re-Check (Post-Design)

All principles remain satisfied after detailed design:

| Principle | Status | Verification |
|-----------|--------|--------------|
| I. Inbox-First | ✅ | Posts enter via `/Approved/Social/` |
| II. Schema Compliance | ✅ | All posts have required YAML frontmatter |
| III. Claim-By-Move | ✅ | Orchestrator processes from `/Approved/Social/` |
| IV. HITL | ✅ | Move to `/Approved/Social/` = approval |
| V. Phase Lock | ✅ | Phase 2 complete prerequisite |
| VI. Audit Logging | ✅ | All actions logged per platform |
| VII. Weekly Audit | ✅ | Engagement metrics in briefings |
| VIII. Modular Skills | ✅ | Meta/Twitter skills with standard interface |
| IX. Ralph Wiggum | ✅ | Error recovery with retry + escalation |
| X. Minimalist Design | ✅ | Image validation in skills |

**GATE RESULT**: ✅ PASS - Design verified against Constitution.

## Next Steps

Proceed to `/sp.tasks` to break this plan into implementation tasks.
