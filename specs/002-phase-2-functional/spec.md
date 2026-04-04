# Feature Specification: Phase 2 Functional - External Communication Senses

**Feature Branch**: `002-phase-2-functional`
**Created**: 2026-03-28
**Status**: Draft
**Input**: Activate external communication 'Senses' and LinkedIn posting capability

## User Scenarios & Testing

### User Story 1 - Gmail Email Alerts (Priority: P1)

As a business owner, I want unread Gmail emails to automatically appear as task alerts in `/Needs_Action` so that I never miss important communications and can prioritize responses effectively.

**Why this priority**: Email is the primary business communication channel. Missing emails can result in lost opportunities, delayed payments, and damaged client relationships.

**Independent Test**: Can be fully tested by sending a test email to the connected Gmail account and verifying a corresponding `.md` alert file appears in `/Needs_Action` within 5 minutes with correct metadata (sender, subject, priority).

**Acceptance Scenarios**:

1. **Given** a new email arrives in Gmail, **When** the Gmail watcher runs, **Then** a `.md` alert file is created in `/Needs_Action` within 5 minutes
2. **Given** an email from a known contact, **When** processed, **Then** the alert includes sender name, subject, received timestamp, and priority level
3. **Given** an email containing "invoice" or "payment" in the subject, **When** processed, **Then** the alert is tagged as high priority and flagged for accounting review
4. **Given** an email is already processed, **When** the watcher runs again, **Then** the same email is not processed twice (no duplicate alerts)

---

### User Story 2 - LinkedIn Post Workflow with HITL (Priority: P1)

As a business owner, I want to draft LinkedIn posts in `/In_Progress` and approve them by moving to `/Approved` before publishing so that all public communications are reviewed for quality and brand alignment.

**Why this priority**: Public posts represent the business brand. HITL (Human-in-the-Loop) approval prevents embarrassing mistakes, ensures brand consistency, and maintains professional standards.

**Independent Test**: Can be fully tested by creating a draft post in `/In_Progress`, moving it to `/Approved`, and verifying the post appears on LinkedIn within 10 minutes.

**Acceptance Scenarios**:

1. **Given** a draft post in `/In_Progress/linkedin-agent/`, **When** I review and approve it, **Then** I move it to `/Approved` and the post is published to LinkedIn
2. **Given** a post has not been moved to `/Approved`, **When** the LinkedIn agent runs, **Then** the post is NOT published (HITL gate enforced)
3. **Given** a post includes an image, **When** reviewed, **Then** the image follows minimalist design rules (dark theme, clean typography, no human icons)
4. **Given** a post is rejected, **When** I move it to `/Rejected`, **Then** the post is not published and includes my feedback for revision

---

### User Story 3 - Communication Triage by Priority (Priority: P2)

As a business owner, I want incoming Gmail and LinkedIn messages to be automatically categorized by priority (High/Low) so that I can focus on urgent communications first and batch-process routine messages.

**Why this priority**: Communication overload reduces productivity. Automatic triage ensures urgent matters get immediate attention while routine messages are batched for efficient processing.

**Independent Test**: Can be fully tested by sending emails with different keywords and verifying the priority tags in `/Needs_Action` alerts match the expected categorization.

**Acceptance Scenarios**:

1. **Given** an email with "urgent", "asap", or "invoice" in subject, **When** processed, **Then** the alert is tagged as high priority
2. **Given** an email from a VIP contact (client, partner), **When** processed, **Then** the alert is tagged as high priority
3. **Given** a routine newsletter or notification, **When** processed, **Then** the alert is tagged as low priority
4. **Given** a LinkedIn message with "partnership" or "opportunity", **When** processed, **Then** the alert is tagged as high priority

---

### User Story 4 - Social Media Metadata Schema (Priority: P2)

As a business owner, I want social media posts to include structured metadata (Platform, Content, Media_Path, Scheduled_Time) so that posts are consistent, trackable, and can be scheduled for optimal engagement times.

**Why this priority**: Structured metadata enables automation, scheduling, and analytics. Without it, posts are ad-hoc, untrackable, and miss optimal posting windows.

**Independent Test**: Can be fully tested by creating a draft post and verifying the YAML frontmatter includes all required metadata fields with correct values.

**Acceptance Scenarios**:

1. **Given** a new post draft, **When** created, **Then** the YAML frontmatter includes: platform, content, media_path (if applicable), scheduled_time, status
2. **Given** a post is scheduled for a specific time, **When** the scheduled time arrives, **Then** the post is published automatically (if already approved)
3. **Given** a post includes an image, **When** processed, **Then** the media_path points to the correct file location
4. **Given** a post is published, **When** completed, **Then** the status is updated to "published" and moved to `/Done`

---

### Edge Cases

- What happens when Gmail API credentials expire? → Alert user to re-authenticate, pause Gmail watcher, log error to audit
- How does the system handle LinkedIn API rate limits? → Queue posts, retry after cooldown period (15 minutes), notify user if queue exceeds 5 posts
- What happens if a post in `/Approved` has invalid metadata? → Log error, move to `/Rejected` with error message, notify user
- How are duplicate emails handled (same sender, same subject)? → Check message ID, skip if already processed, log as duplicate
- What if the user moves a post back from `/Approved` to `/In_Progress`? → Treat as revision request, update status, do not publish

## Requirements

### Functional Requirements

- **FR-001**: System MUST connect to Gmail API using credentials.json from Phase 1
- **FR-002**: System MUST monitor Gmail for unread emails every 5 minutes
- **FR-003**: System MUST create `.md` alert files in `/Needs_Action` for each new email
- **FR-004**: Email alerts MUST include metadata: sender, subject, received_timestamp, priority, message_id
- **FR-005**: System MUST categorize emails by priority (High/Low) based on keywords and sender
- **FR-006**: System MUST provide LinkedIn posting capability via Playwright MCP or LinkedIn API
- **FR-007**: LinkedIn posts MUST require HITL approval (move to `/Approved` before publishing)
- **FR-008**: Posts MUST include metadata: platform, content, media_path, scheduled_time, status
- **FR-009**: System MUST enforce minimalist design rules for image-based posts (dark theme, clean typography)
- **FR-010**: System MUST track processed emails to prevent duplicate alerts (by message_id)
- **FR-011**: System MUST queue posts when API rate limits are hit and retry after cooldown
- **FR-012**: System MUST log all actions (email processed, post drafted, post published) to audit log
- **FR-013**: System MUST support post scheduling (publish at scheduled_time automatically)
- **FR-014**: Rejected posts MUST include user feedback for revision
- **FR-015**: System MUST handle credential expiry gracefully (alert user, pause watcher, log error)

### Key Entities

- **Email Alert**: `.md` file in `/Needs_Action` representing an unread Gmail message with metadata (sender, subject, priority, message_id)
- **Social Media Post**: `.md` file representing a draft/approved/published post with metadata (platform, content, media_path, scheduled_time, status)
- **Communication Triage**: Classification logic that assigns priority (High/Low) to incoming messages based on keywords, sender, and content
- **HITL Gate**: Approval workflow requiring human to move post from `/In_Progress` to `/Approved` before publishing
- **Credential Store**: Secure storage for Gmail API and LinkedIn API credentials (credentials.json, .env)

## Success Criteria

- **SC-001**: Email alerts appear in `/Needs_Action` within 5 minutes of arrival in Gmail (95% of the time)
- **SC-002**: Zero duplicate email alerts (each email processed exactly once)
- **SC-003**: 100% of LinkedIn posts require HITL approval before publishing (no bypass possible)
- **SC-004**: High-priority emails correctly identified 90% of the time (based on keywords/sender)
- **SC-005**: Scheduled posts published within 2 minutes of scheduled_time
- **SC-006**: Zero posts published with invalid metadata (all required fields present)
- **SC-007**: User can process 50+ emails per day without manual sorting (auto-triage effective)
- **SC-008**: All social media posts follow minimalist design guidelines (100% compliance)
- **SC-009**: Credential expiry detected and user alerted within 1 minute (no silent failures)
- **SC-010**: API rate limits handled gracefully (posts queued, user notified if queue > 5)

## Assumptions

- User has Gmail API credentials set up (credentials.json from Phase 1)
- User has LinkedIn account with posting permissions
- Gmail API quota sufficient for monitoring (1 email check per 5 minutes)
- LinkedIn API access available (or Playwright MCP for browser automation)
- User checks `/Needs_Action` at least once daily for email alerts
- User reviews `/Approved` folder at least once daily for pending posts
- Internet connection available for API calls
- Phase 1 Foundation is complete (vault structure, audit logging, HITL workflow)
