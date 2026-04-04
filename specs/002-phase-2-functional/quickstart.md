# Quickstart: Phase 2 Functional

**Feature**: 002-phase-2-functional  
**Last Updated**: 2026-03-28  
**Status**: Draft

## Overview

Phase 2 Functional adds external communication capabilities:
- **Gmail Watcher**: Monitors unread emails, creates alerts in `/Needs_Action`
- **LinkedIn Poster**: Draft posts in `/In_Progress`, approve in `/Approved`, publish via Playwright
- **Communication Triage**: Auto-categorize messages by priority (High/Low)
- **Social Media Metadata**: Structured post metadata for scheduling and tracking

## Prerequisites

- Phase 1 Foundation complete (vault structure, audit logging, HITL workflow)
- Python 3.11 or higher
- Gmail API credentials (credentials.json)
- LinkedIn account with posting permissions
- Obsidian (or any Markdown editor)

## Installation

### Step 1: Install Python Dependencies

```bash
cd E:\hackathon_0_digital_fte\AI_Employee_vault
pip install -r requirements.txt
```

**New dependencies for Phase 2**:
- `google-auth-oauthlib` (Gmail OAuth2)
- `google-api-python-client` (Gmail API)
- `playwright` (LinkedIn browser automation)

### Step 2: Install Playwright Browsers

```bash
playwright install chromium
```

### Step 3: Setup Gmail API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Gmail API
4. Create OAuth2 credentials (Desktop app)
5. Download `credentials.json`
6. Place in vault root: `E:\hackathon_0_digital_fte\AI_Employee_vault\credentials.json`

**Note**: `credentials.json` is gitignored for security.

### Step 4: Authenticate Gmail

Run the Gmail authentication script:

```bash
python src/gmail/gmail_watcher.py --authenticate
```

This will:
1. Open browser for Google login
2. Request Gmail read permissions
3. Save OAuth2 tokens to `credentials.json`

### Step 5: Configure Triage Rules

Edit `/config/triage_rules.yaml`:

```yaml
priority_keywords:
  high:
    - urgent
    - asap
    - invoice
    - payment
  low:
    - newsletter
    - notification

vip_senders:
  - client@company.com
  - boss@company.com
```

## Usage

### Gmail Watcher

#### Start the Watcher

```bash
python src/gmail/gmail_watcher.py
```

The watcher will:
1. Connect to Gmail API
2. Check for unread emails every 5 minutes
3. Create `.md` alert files in `/Needs_Action`
4. Mark emails as processed (no duplicates)
5. Log all actions to `/Logs/YYYY-MM-DD.json`

#### Test the Watcher

1. Send a test email to your Gmail account
2. Wait up to 5 minutes
3. Check `/Needs_Action` for alert file:
   ```bash
   dir Needs_Action\email-*.md
   ```
4. View the alert:
   ```markdown
   ---
   status: Needs_Action
   type: email_alert
   sender: sender@example.com
   subject: Test Email
   received_timestamp: 2026-03-28T10:30:00Z
   priority: normal
   ---
   
   ## Email Content
   
   **From**: sender@example.com
   **Date**: 2026-03-28 10:30 AM
   
   This is a test email.
   ```

### LinkedIn Post Workflow

#### Create a Draft Post

Drafts are created in `/In_Progress/linkedin-agent/`:

```markdown
---
status: draft
platform: linkedin
content: |
  Excited to announce our new AI Employee automation system!
  
  #Automation #AI
media_path: ./media/announcement.png
scheduled_time: 2026-03-29T09:00:00Z
created_at: 2026-03-28T14:00:00Z
created_by: linkedin-agent
hitl_approved: false
---

## Post Preview

**Platform**: LinkedIn
**Scheduled**: 2026-03-29 09:00 AM
```

#### Approve a Post (HITL)

1. Review draft in `/In_Progress/linkedin-agent/`
2. If approved, move file to `/Approved/`
3. LinkedIn publisher will automatically publish within 10 minutes

#### Publish Immediately

For immediate publishing (no scheduling):

1. Create draft without `scheduled_time`
2. Move to `/Approved/`
3. Run publisher manually:
   ```bash
   python src/linkedin/linkedin_publisher.py
   ```

#### Check Publishing Status

View audit log:
```bash
type Logs\2026-03-28.json | findstr linkedin
```

### Communication Triage

#### How Priority is Assigned

Emails are categorized based on:
1. **VIP senders**: Always high priority
2. **Keywords**: Subject line matching (invoice, urgent → high)
3. **Domains**: Newsletter domains → low priority

#### Test Triage

Send emails with different subjects:
- "Invoice #2026-001" → High priority alert
- "URGENT: Meeting Tomorrow" → High priority alert
- "Weekly Newsletter" → Low priority alert

Check alert metadata:
```bash
type Needs_Action\email-*.md | findstr priority
```

### Social Media Metadata

#### Required Fields

All posts MUST include:
- `status`: draft, approved, published, rejected
- `platform`: linkedin, twitter, facebook
- `content`: Post text
- `created_at`: ISO 8601 timestamp
- `created_by`: Agent identifier
- `hitl_approved`: false (until moved to /Approved)

#### Optional Fields

- `media_path`: Path to image/media
- `scheduled_time`: When to publish
- `tags`: Post categorization

## Troubleshooting

### Gmail Watcher Not Detecting Emails

1. **Check credentials**:
   ```bash
   type credentials.json
   ```
   Should contain OAuth2 tokens.

2. **Re-authenticate**:
   ```bash
   python src/gmail/gmail_watcher.py --authenticate
   ```

3. **Check Gmail API quota**:
   - Visit Google Cloud Console
   - Check Gmail API usage

### LinkedIn Publisher Fails

1. **Check Playwright installation**:
   ```bash
   playwright install chromium
   ```

2. **Verify LinkedIn login**:
   - Publisher runs in non-headless mode
   - Watch for login prompt
   - Complete 2FA if required

3. **Check HITL gate**:
   - Post MUST be in `/Approved/`
   - `hitl_approved` MUST be `true`

### Duplicate Email Alerts

1. **Check processed_emails.json**:
   ```bash
   type Logs\processed_emails.json
   ```

2. **Clear processed log** (if needed):
   ```bash
   del Logs\processed_emails.json
   ```

### Priority Classification Incorrect

1. **Review triage rules**:
   ```bash
   type config\triage_rules.yaml
   ```

2. **Add missing keywords**:
   Edit `config/triage_rules.yaml`, add keywords to appropriate list.

3. **Add VIP sender**:
   Add sender email to `vip_senders` list.

## Next Steps

### Phase 2 Completion Checklist

- [ ] Gmail watcher detects emails within 5 minutes
- [ ] Email alerts include all required metadata
- [ ] Priority classification accurate (90%+)
- [ ] LinkedIn draft posts created in `/In_Progress`
- [ ] HITL workflow enforced (only `/Approved` posts published)
- [ ] Posts follow minimalist design rules
- [ ] All actions logged to audit

### Phase 3 Preparation

Once Phase 2 is complete, you're ready for:
- Odoo Accounting integration
- Business Audit automation
- Ralph Wiggum reasoning loops
- Daily briefings in `/Briefings/`

## Support

For issues or questions:
1. Check audit logs: `/Logs/YYYY-MM-DD.json`
2. Review Constitution: `.specify/memory/constitution.md`
3. Consult data model: `specs/002-phase-2-functional/data-model.md`
