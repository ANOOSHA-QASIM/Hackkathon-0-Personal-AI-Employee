# Feature Specification: Phase 3 Social Media Suite

**Feature Branch**: `003-phase-3-social-media-suite`
**Created**: 2026-03-28
**Status**: Draft
**Input**: Implement Gold Tier Social Media Suite (Facebook, Instagram, Twitter/X)

## User Scenarios & Testing

### User Story 1 - Cross-Platform Social Posting (Priority: P1)

As a business owner, I want to create a single post and have it automatically published to all 4 platforms (LinkedIn, Facebook, Instagram, Twitter/X) so that I can maintain a consistent social media presence without manual cross-posting.

**Why this priority**: Manual cross-posting is time-consuming and error-prone. Automated multi-platform posting ensures consistent brand messaging and saves hours of repetitive work.

**Independent Test**: Can be fully tested by creating a post file in `/Approved/Social/` and verifying it appears on all 4 platforms within 10 minutes.

**Acceptance Scenarios**:

1. **Given** a post file is moved to `/Approved/Social/`, **When** the orchestrator runs, **Then** the post is published to all 4 platforms (LinkedIn, Facebook, Instagram, Twitter)
2. **Given** a post includes an image, **When** published, **Then** the image appears correctly on all platforms that support images
3. **Given** a post is too long for Twitter, **When** published, **Then** it is automatically split into a thread
4. **Given** one platform fails (e.g., Twitter API limit), **When** the Ralph Wiggum loop runs, **Then** the error is logged and retried after 15 minutes without human intervention

---

### User Story 2 - Meta Platform Integration (Priority: P1)

As a business owner, I want Facebook and Instagram posts to be managed through a unified Meta poster with persistent browser sessions so that I don't need to re-authenticate for every post.

**Why this priority**: Persistent sessions reduce authentication friction and enable reliable automated posting to Meta platforms without manual intervention.

**Independent Test**: Can be fully tested by logging in once to Facebook/Instagram, then verifying subsequent posts publish without requiring re-authentication.

**Acceptance Scenarios**:

1. **Given** the first Meta post, **When** the poster runs, **Then** a browser window opens for manual login
2. **Given** login is successful, **When** the session is saved to `.browser_data/meta`, **Then** subsequent posts use the saved session without requiring login
3. **Given** a post includes an image, **When** published to Instagram, **Then** the image is uploaded correctly from the `media_path`
4. **Given** the session expires, **When** the poster detects expiration, **Then** it requests re-authentication and saves the new session

---

### User Story 3 - Twitter (X) Integration (Priority: P2)

As a business owner, I want Twitter (X) posts to support both single tweets and auto-threading for long content so that I can share detailed updates without manual thread creation.

**Why this priority**: Twitter's character limit requires threading for longer content. Auto-threading enables detailed business updates without manual effort.

**Independent Test**: Can be fully tested by creating a post with >280 characters and verifying it appears as a properly formatted thread on Twitter.

**Acceptance Scenarios**:

1. **Given** a post under 280 characters, **When** published to Twitter, **Then** it appears as a single tweet
2. **Given** a post over 280 characters, **When** published to Twitter, **Then** it is automatically split into a threaded sequence
3. **Given** a post includes an image, **When** published to Twitter, **Then** the image is attached to the first tweet in the thread
4. **Given** Twitter API rate limit is hit, **When** the Ralph Wiggum loop runs, **Then** the post is queued and retried after 15 minutes

---

### User Story 4 - Ralph Wiggum Error Recovery (Priority: P2)

As a business owner, I want failed posts to be automatically retried with intelligent error recovery so that temporary issues (API limits, network problems) don't require manual intervention.

**Why this priority**: Transient failures are common in social media APIs. Automatic recovery ensures posts are eventually published without human oversight.

**Independent Test**: Can be fully tested by simulating an API failure and verifying the post is retried and eventually published after the cooldown period.

**Acceptance Scenarios**:

1. **Given** a platform API returns a rate limit error, **When** the Ralph Wiggum loop detects it, **Then** the error is logged and the post is queued for retry
2. **Given** a post is queued for retry, **When** 15 minutes have elapsed, **Then** the post is automatically retried
3. **Given** all 3 retry attempts are exhausted, **When** the loop completes, **Then** the error is escalated to `/Needs_Action/` for human review
4. **Given** one platform fails but others succeed, **When** the orchestrator completes, **Then** successful posts are confirmed and failed platform is retried independently

---

### Edge Cases

- What happens when an image file in `media_path` doesn't exist? → Log error, publish text-only post, flag missing image for review
- How does the system handle platform-specific content restrictions? → Validate content against platform rules before posting, flag violations for human review
- What happens if the browser session is corrupted? → Detect corruption, delete session file, request fresh authentication
- How are very long posts handled on Instagram? → Truncate with ellipsis, flag for manual review if >2200 characters
- What if the orchestrator crashes mid-posting? → On restart, check `/Approved/Social/` for unprocessed files, resume from last successful platform

## Requirements

### Functional Requirements

- **FR-001**: System MUST provide a Meta Poster skill (`src/skills/meta_poster.py`) for Facebook and Instagram posting
- **FR-002**: Meta Poster MUST use Playwright with persistent session stored in `.browser_data/meta`
- **FR-003**: System MUST provide a Twitter Poster skill (`src/skills/twitter_poster.py`) for X (Twitter) posting
- **FR-004**: Twitter Poster MUST support single tweets and auto-threading for content >280 characters
- **FR-005**: System MUST provide a Cross-Platform Orchestrator that triggers all 4 platforms when a file enters `/Approved/Social/`
- **FR-006**: Orchestrator MUST publish to LinkedIn, Facebook, Instagram, and Twitter in sequence
- **FR-007**: All platforms MUST correctly handle image attachments from `media_path` metadata field
- **FR-008**: Ralph Wiggum logic MUST retry failed platforms after 15-minute cooldown (max 3 attempts)
- **FR-009**: Ralph Wiggum logic MUST log all errors to `/Logs/YYYY-MM-DD.json` with platform and error details
- **FR-010**: After 3 failed retries, Ralph Wiggum MUST escalate to `/Needs_Action/` for human review
- **FR-011**: System MUST track posting status per platform (pending, published, failed, retrying)
- **FR-012**: System MUST update post metadata with platform-specific results (post URLs, timestamps)
- **FR-013**: Successful posts MUST be moved to `/Done/Social/` with completion timestamp
- **FR-014**: Failed posts MUST remain in `/Approved/Social/` with failure metadata for retry

### Key Entities

- **Social Media Post**: `.md` file in `/Approved/Social/` with content, media_path, and platform-specific metadata
- **Platform Skill**: Modular skill for each platform (LinkedIn, Facebook, Instagram, Twitter) with standard interface
- **Cross-Platform Orchestrator**: Coordinates posting across all 4 platforms with error handling
- **Ralph Wiggum Loop**: Autonomous error recovery with exponential backoff and escalation
- **Persistent Session**: Browser session data stored in `.browser_data/` for reuse without re-authentication

## Success Criteria

- **SC-001**: 95% of posts are successfully published to all 4 platforms within 10 minutes of approval
- **SC-002**: Auto-threading correctly splits long content for Twitter 100% of the time
- **SC-003**: Image attachments are correctly uploaded to all platforms 95% of the time
- **SC-004**: Ralph Wiggum error recovery succeeds 90% of the time without human intervention
- **SC-005**: Persistent sessions reduce authentication time from 2 minutes to <10 seconds for 95% of posts
- **SC-006**: Zero posts are duplicated across platforms (each post published exactly once per platform)
- **SC-007**: All posting errors are logged with sufficient detail for debugging 100% of the time
- **SC-008**: User can post to all 4 platforms by moving a single file to `/Approved/Social/`

## Assumptions

- User has active accounts on LinkedIn, Facebook, Instagram, and Twitter (X)
- User has necessary API access or browser automation permissions for all platforms
- Phase 2 (LinkedIn posting) is complete and functional
- Persistent browser sessions are stored securely in `.browser_data/`
- Internet connection is available for API calls and browser automation
- Platform API rate limits are within acceptable ranges for business posting frequency
- Images in `media_path` are in supported formats (JPG, PNG) and under platform size limits
