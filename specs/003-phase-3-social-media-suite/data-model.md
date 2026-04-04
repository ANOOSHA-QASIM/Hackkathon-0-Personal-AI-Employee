# Data Model: Phase 3 Social Media Suite

**Feature**: 003-phase-3-social-media-suite  
**Date**: 2026-03-28  
**Status**: Draft

## Overview

This document defines the core data entities for Phase 3 Social Media Suite (Meta/Facebook/Instagram, Twitter/X, cross-platform orchestration, Ralph Wiggum error recovery). All entities are file-based (Markdown with YAML frontmatter, JSON session data) per the Constitution's file-based state persistence principle.

---

## Entity 1: SocialMediaPost

**Purpose**: YAML frontmatter schema for social media post files in `/Approved/Social/`.

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `status` | string | ✅ | Post state | `draft`, `approved`, `published`, `failed` |
| `platforms` | array[string] | ✅ | Target platforms | `["linkedin", "facebook", "instagram", "twitter"]` |
| `content` | string | ✅ | Post text content | `"Excited to announce..."` |
| `media_path` | string | ❌ | Path to image/media file | `./media/post-image.png` |
| `scheduled_time` | string (ISO 8601) | ❌ | When to publish | `2026-03-29T09:00:00Z` |
| `created_at` | string (ISO 8601) | ✅ | When draft created | `2026-03-28T14:00:00Z` |
| `created_by` | string | ✅ | Who created draft | `user` or `social-media-agent` |
| `platform_results` | object | ❌ | Per-platform results | See below |

### Platform Results Structure

```yaml
platform_results:
  linkedin:
    status: published  # pending, published, failed, retrying
    url: https://linkedin.com/feed/update/...
    published_at: 2026-03-28T15:00:00Z
    error: null
  facebook:
    status: failed
    url: null
    published_at: null
    error: "Session expired - re-authentication required"
  instagram:
    status: pending
    url: null
    published_at: null
    error: null
  twitter:
    status: retrying
    url: null
    published_at: null
    error: "Rate limit exceeded - retry in 15 minutes"
```

### Example

```yaml
---
status: approved
platforms:
  - linkedin
  - facebook
  - instagram
  - twitter
content: |
  Excited to announce our new AI Employee automation system!
  
  This system combines Gmail monitoring, task management, and automated posting to help businesses scale efficiently.
  
  #Automation #AI #Productivity
media_path: ./media/announcement-dark.png
scheduled_time: 2026-03-29T09:00:00Z
created_at: 2026-03-28T14:00:00Z
created_by: user
platform_results: {}
---

## Post Preview

**Platforms**: LinkedIn, Facebook, Instagram, Twitter
**Scheduled**: 2026-03-29 09:00 AM
**Media**: See attached image

---

## HITL Approval

**To Approve**: Move this file to `/Approved/Social/` folder

**To Reject**: Move this file to `/Rejected/` folder with feedback below

- [ ] Approved (move to /Approved/Social)
- [ ] Rejected (move to /Rejected with feedback)

**Feedback**: 
```

### Validation Rules

1. `status` MUST be one of: `draft`, `approved`, `published`, `failed`
2. `platforms` MUST contain at least one platform
3. `content` MUST be 1-3000 characters (LinkedIn limit)
4. If `media_path` present, image MUST follow minimalist design rules (Constitution Principle X)
5. `platform_results` tracks per-platform status independently

### State Transitions

```
draft → approved (user moves to /Approved/Social)
approved → published (all platforms succeed)
approved → failed (all platforms fail after 3 retries)
approved → partial (some platforms succeed, some fail)
failed → draft (user edits and resubmits)
```

---

## Entity 2: PlatformSkill

**Purpose**: Standard interface for all platform posting skills (LinkedIn, Meta, Twitter).

### Interface Definition

```python
from abc import ABC, abstractmethod

class PlatformSkill(ABC):
    """Base class for all platform posting skills."""
    
    def __init__(self, platform_name: str, user_data_dir: Path):
        self.platform_name = platform_name
        self.user_data_dir = user_data_dir
        self.context = None
    
    @abstractmethod
    def post(self, content: str, media_path: str = None) -> PostingResult:
        """
        Post content to platform.
        
        Args:
            content: Post text content
            media_path: Optional path to image/media file
        
        Returns:
            PostingResult with status, URL, timestamps, errors
        """
        pass
    
    @abstractmethod
    def authenticate(self) -> bool:
        """
        Authenticate with platform.
        
        Returns:
            True if authentication successful
        """
        pass
    
    def close(self):
        """Close browser context."""
        if self.context:
            self.context.close()
```

### Concrete Implementations

- **LinkedInPoster** (`src/skills/linkedin_poster.py`) - Phase 2
- **MetaPoster** (`src/skills/meta_poster.py`) - Phase 3 (Facebook + Instagram)
- **TwitterPoster** (`src/skills/twitter_poster.py`) - Phase 3 (X)

---

## Entity 3: PostingResult

**Purpose**: Result of posting attempt to a single platform.

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `platform` | string | ✅ | Platform name | `linkedin`, `facebook`, `instagram`, `twitter` |
| `status` | string | ✅ | Post status | `pending`, `published`, `failed`, `retrying` |
| `url` | string | ❌ | Post URL (if published) | `https://linkedin.com/feed/update/...` |
| `published_at` | string (ISO 8601) | ❌ | When published | `2026-03-28T15:00:00Z` |
| `error` | string | ❌ | Error message (if failed) | `"Session expired"` |
| `retry_count` | integer | ❌ | Number of retry attempts | `2` |
| `next_retry_at` | string (ISO 8601) | ❌ | When to retry | `2026-03-28T15:15:00Z` |

### Example

```python
PostingResult(
    platform='twitter',
    status='retrying',
    url=None,
    published_at=None,
    error='Rate limit exceeded - retry in 15 minutes',
    retry_count=2,
    next_retry_at='2026-03-28T15:15:00Z'
)
```

---

## Entity 4: RalphWiggumState

**Purpose**: State tracking for Ralph Wiggum error recovery loop.

### Fields

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `post_file` | string | ✅ | Path to post file | `/Approved/Social/post-001.md` |
| `platform` | string | ✅ | Platform that failed | `twitter` |
| `error` | string | ✅ | Last error message | `Rate limit exceeded` |
| `retry_count` | integer | ✅ | Number of retries attempted | `1` |
| `max_retries` | integer | ✅ | Maximum retry attempts | `3` |
| `cooldown_seconds` | integer | ✅ | Seconds between retries | `900` (15 minutes) |
| `last_attempt_at` | string (ISO 8601) | ✅ | When last retry attempted | `2026-03-28T15:00:00Z` |
| `next_retry_at` | string (ISO 8601) | ✅ | When next retry allowed | `2026-03-28T15:15:00Z` |
| `escalated` | boolean | ✅ | Whether escalated to human | `false` |

### State Transitions

```
initial → retrying (first failure)
retrying → retrying (retry failed, increment count)
retrying → success (retry succeeded)
retrying → escalated (max retries exhausted)
escalated → draft (human edits and resubmits)
```

---

## Entity 5: PersistentSession

**Purpose**: Browser session data stored in `.browser_data/` for reuse.

### Storage Location

```
.browser_data/
├── linkedin/     # Phase 2
├── meta/         # Phase 3 (Facebook + Instagram)
└── twitter/      # Phase 3 (X)
```

### Session Contents

- Cookies (authentication tokens)
- Local storage (platform-specific data)
- Browser profile (user agent, viewport settings)

### Session Lifecycle

1. **First post**: Browser opens for manual login, session saved
2. **Subsequent posts**: Session reused, no login required
3. **Session expired**: Detect expiration, request re-authentication, save new session
4. **Session corrupted**: Delete session file, request fresh authentication

---

## Relationships

```
SocialMediaPost
├── posted_by → PlatformSkill[] (LinkedIn, Meta, Twitter)
├── results_in → PostingResult[] (one per platform)
├── recovered_by → RalphWiggumState (on failure)
└── uses_session → PersistentSession (per platform)

PlatformSkill
├── inherits → BasePoster (standard interface)
├── produces → PostingResult
└── uses → PersistentSession

RalphWiggumState
├── tracks → SocialMediaPost
├── retries → PlatformSkill.post()
└── escalates_to → /Needs_Action/ (on max retries)
```

---

## File Locations

| Entity | Storage Format | Location |
|--------|---------------|----------|
| SocialMediaPost | YAML frontmatter | `/Approved/Social/*.md` |
| PostingResult | Embedded in post metadata | `platform_results` field |
| RalphWiggumState | JSON (in-memory or file) | `/Logs/ralph_wiggum_state.json` |
| PersistentSession | Browser data directory | `.browser_data/{platform}/` |

---

## Schema Evolution

### Phase 3 (Current)
- SocialMediaPost: Multi-platform support, per-platform results
- PlatformSkill: Modular skills architecture
- RalphWiggumState: Error recovery with retry + escalation

### Phase 4+ (Future)
- SocialMediaPost: Add `engagement_metrics` (likes, shares, comments)
- PlatformSkill: Add `get_engagement()` method for analytics
- RalphWiggumState: Add `smart_retry` (different strategy based on error type)
