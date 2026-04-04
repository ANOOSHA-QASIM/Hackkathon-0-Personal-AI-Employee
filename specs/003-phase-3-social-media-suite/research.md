# Technical Research: Phase 3 Social Media Suite

**Feature**: 003-phase-3-social-media-suite  
**Date**: 2026-03-28  
**Status**: Complete

## Research Summary

This document resolves all technical unknowns for Phase 3 Social Media Suite (Meta/Facebook/Instagram, Twitter/X, cross-platform orchestration, Ralph Wiggum error recovery). Each section includes the decision made, rationale, and alternatives considered.

---

## 1. Meta (Facebook/Instagram) Automation Pattern

**Question**: What is the best approach for posting to Facebook and Instagram?

### Decision
Use **Playwright** for both Facebook and Instagram with unified Meta account and persistent session in `.browser_data/meta`.

### Rationale
- **Consistent with Phase 2**: Same Playwright approach as LinkedIn poster
- **No API approval needed**: Avoids Facebook app review process (can take weeks)
- **Unified session**: Single login covers both Facebook and Instagram
- **Image support**: Full control over image upload flow
- **Persistent sessions**: Login once, post many times without re-authentication

### Implementation Pattern
```python
from playwright.sync_api import sync_playwright

class MetaPoster:
    def __init__(self):
        self.user_data_dir = VAULT_ROOT / '.browser_data' / 'meta'
        self.context = None
    
    def _launch_browser(self):
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(self.user_data_dir),
            headless=False,
            timeout=90000
        )
        return context
    
    def post_to_facebook(self, content, image_path=None):
        # Navigate to Facebook, post content, upload image if provided
        pass
    
    def post_to_instagram(self, content, image_path=None):
        # Navigate to Instagram, post content, upload image if provided
        pass
```

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Facebook Graph API | Official, stable | App review required (2-4 weeks), limited Instagram posting | Too slow for Phase 3 timeline |
| Instagram Basic Display API | Official Instagram | Read-only (no posting), limited scope | Cannot post, only display |
| Third-party services (Buffer, Hootsuite) | Easy integration | Monthly cost, security concerns (store credentials externally) | Violates Phase 1 security principles |

---

## 2. Twitter (X) Automation Pattern

**Question**: What is the best approach for posting to Twitter (X)?

### Decision
Use **Playwright** for posting (primary), with Tweepy as optional fallback for API-based posting.

### Rationale
- **Consistent with other platforms**: Same Playwright approach as LinkedIn, Meta
- **Handles auth seamlessly**: Browser-based login, no API key management
- **Auto-threading support**: Full control over thread creation flow
- **Image support**: Native image upload through browser interface
- **No API rate limits**: Browser automation not subject to API rate limits

### Implementation Pattern
```python
class TwitterPoster:
    def __init__(self):
        self.user_data_dir = VAULT_ROOT / '.browser_data' / 'twitter'
        self.max_tweet_length = 280
    
    def _split_into_thread(self, content):
        """Split content into 280-char tweets."""
        tweets = []
        while len(content) > self.max_tweet_length:
            # Find last space before 280 chars
            split_point = content.rfind(' ', 0, self.max_tweet_length)
            if split_point == -1:
                split_point = self.max_tweet_length
            tweets.append(content[:split_point])
            content = content[split_point:].strip()
        tweets.append(content)
        return tweets
    
    def post_tweet_thread(self, content, image_path=None):
        # Login, split content, post thread, attach image to first tweet
        pass
```

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Twitter API v2 (Tweepy) | Official, fast | Requires developer account, rate limits (300 tweets/day), API key management | Playwright more consistent with other platforms |
| Third-party services | Easy integration | Monthly cost, less control over threading | Playwright provides full control |

---

## 3. Auto-Threading Strategy

**Question**: How should long content be split into Twitter threads?

### Decision
Split at **280 characters** (Twitter limit), continue thread with "..." separator between tweets.

### Rationale
- **Standard pattern**: Matches how Twitter users manually create threads
- **Preserves readability**: "..." indicates continuation
- **Simple implementation**: No complex sentence-boundary detection needed
- **Handles edge cases**: Works with any content type

### Implementation Pattern
```python
def _split_into_thread(self, content, max_length=280):
    """Split content into thread of tweets."""
    tweets = []
    remaining = content.strip()
    
    while len(remaining) > max_length:
        # Find last space before max_length
        split_point = remaining.rfind(' ', 0, max_length)
        if split_point == -1:
            # No space found, hard split
            split_point = max_length
        
        tweet = remaining[:split_point].strip()
        if tweets:  # Not first tweet
            tweet = "... " + tweet  # Add continuation marker
        
        tweets.append(tweet)
        remaining = remaining[split_point:].strip()
    
    # Last tweet
    if tweets:
        remaining = "... " + remaining
    tweets.append(remaining)
    
    return tweets
```

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Split at sentence boundaries | More readable | Complex implementation, may exceed 280 chars | Simple char limit more reliable |
| Manual thread markers (e.g., "1/", "2/") | Explicit numbering | Requires user to format content manually | Auto-splitting more user-friendly |
| Fixed 275 chars (leave buffer) | Safer for emoji/special chars | Wastes character limit | 280 exact with fallback to hard split |

---

## 4. Persistent Session Management

**Question**: How should browser sessions be stored and managed across platforms?

### Decision
Store in **`.browser_data/meta`** and **`.browser_data/twitter`** directories, consistent with Phase 2 LinkedIn (`.browser_data/linkedin`).

### Rationale
- **Consistent with Phase 2**: Same pattern as LinkedIn poster
- **Platform isolation**: Each platform has separate session data
- **Persistent across runs**: Login once, post many times
- **Secure**: Session data stays local, not shared externally

### Directory Structure
```
.browser_data/
├── linkedin/     # Phase 2
├── meta/         # Phase 3 (Facebook + Instagram)
└── twitter/      # Phase 3 (X)
```

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Cookie files | Portable, easy to backup | Less secure, harder to manage | Playwright persistent context more robust |
| Manual auth every time | Maximum security | High friction, slows down posting | Persistent sessions reduce auth time from 2min to <10sec |
| OS keychain integration | OS-level security | Platform-specific, complex | Local `.browser_data/` simpler and cross-platform |

---

## 5. Ralph Wiggum Error Recovery

**Question**: How should failed posts be retried automatically?

### Decision
**15-minute cooldown**, **max 3 retries**, then **escalate to `/Needs_Action/`** for human review.

### Rationale
- **15-minute cooldown**: Standard API rate limit recovery window
- **Max 3 retries**: Balances persistence with eventual human oversight
- **Escalation path**: Ensures no post is lost forever
- **Logged errors**: Full audit trail for debugging

### Implementation Pattern
```python
class RalphWiggum:
    def __init__(self, max_retries=3, cooldown_minutes=15):
        self.max_retries = max_retries
        self.cooldown_seconds = cooldown_minutes * 60
    
    def retry_on_failure(self, func, post_file, platform):
        """Retry function on failure with exponential backoff."""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                return func()
            except Exception as e:
                last_error = e
                log_error(platform, str(e), attempt + 1)
                
                if attempt < self.max_retries - 1:
                    print(f"[Ralph Wiggum] Retrying {platform} in {self.cooldown_seconds}s...")
                    time.sleep(self.cooldown_seconds)
        
        # All retries exhausted - escalate to human
        escalate_to_human(post_file, platform, last_error)
        return False
```

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Exponential backoff (1min, 5min, 25min) | More sophisticated | Complex state management | Fixed 15-min simpler and effective |
| Immediate retry | Fast recovery | Risks hitting rate limits again | 15-min cooldown standard for rate limits |
| No retry (fail immediately) | Simple | Poor UX, requires manual intervention for transient errors | Ralph Wiggum autonomy is key Phase 3 feature |

---

## Conclusion

All technical unknowns resolved. Key decisions:
1. **Playwright for Meta** (Facebook + Instagram) - consistent, no API approval
2. **Playwright for Twitter** - consistent, auto-threading support
3. **280-char split with "..."** - standard threading pattern
4. **`.browser_data/` per platform** - persistent sessions, consistent with Phase 2
5. **15-min cooldown, 3 retries, escalate** - balances automation with oversight

Proceed to Phase 1: Generate data-model.md, contracts, and quickstart.md.
