# Phase 2 Functional - Quick Start Guide

**Last Updated**: 2026-03-28  
**Status**: Ready for Testing

## Overview

Phase 2 adds external communication capabilities:
- ✅ **Gmail Monitor**: Unread emails → alerts in `/Needs_Action`
- ✅ **LinkedIn Poster**: Draft posts → HITL approval → auto-publish
- ✅ **Communication Triage**: Auto-categorize by priority (High/Low)
- ✅ **Audit Logging**: All actions logged to `/Logs/YYYY-MM-DD.json`

## Quick Setup (15 minutes)

### Step 1: Install Dependencies

```bash
cd E:\hackathon_0_digital_fte\AI_Employee_vault
pip install -r requirements.txt
playwright install chromium
```

### Step 2: Setup Gmail API (5 minutes)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or select existing
3. Enable **Gmail API**
4. Create **OAuth2 credentials** (Desktop app)
5. Download `credentials.json`
6. Place in vault root: `E:\hackathon_0_digital_fte\AI_Employee_vault\credentials.json`

### Step 3: Authenticate Gmail

```bash
python src/gmail/gmail_auth.py --authenticate
```

This will:
- Open browser for Google login
- Request Gmail read permissions
- Save OAuth2 tokens to `credentials.json`

### Step 4: Test Gmail Connection

```bash
python src/gmail/gmail_auth.py --test
```

Expected output:
```
✓ Connected to Gmail account: your@email.com
✓ Found X unread emails
Gmail API Test: PASSED
```

### Step 5: Configure Triage Rules (Optional)

Edit `config/triage_rules.yaml` to customize:
- VIP senders (always high priority)
- High-priority keywords (invoice, urgent, payment)
- Low-priority keywords (newsletter, notification)

## Usage

### Gmail Monitor

**Option 1: Run continuously**
```bash
run_gmail_monitor.bat
```

**Option 2: Run once (for testing)**
```bash
python src/gmail/gmail_monitor.py --once
```

**Option 3: Use Python module**
```bash
python -m gmail
```

**Test**: Send yourself an email → check `/Needs_Action` for alert

### LinkedIn Poster

**Option 1: Run continuously**
```bash
run_linkedin_poster.bat
```

**Option 2: Run once (for testing)**
```bash
python src/linkedin/linkedin_poster.py --once
```

**Option 3: Use Python module**
```bash
python -m linkedin
```

**Test**:
1. Create draft post (see below)
2. Move to `/Approved/`
3. Run poster
4. Check LinkedIn for your post

### Create LinkedIn Post

**Option 1: Use template**
```bash
python src/linkedin/post_generator.py --template
```

**Option 2: Create from command**
```bash
python src/linkedin/post_generator.py --create "Excited to announce our new AI Employee system! #Automation #AI"
```

**Option 3: Manual**
1. Copy `Briefings/LinkedIn_Post_Template.md`
2. Fill in content
3. Save to `/In_Progress/linkedin-agent/`

### Schedule Post for Later

```bash
python src/linkedin/post_generator.py --create "Your content here" --schedule "2026-03-29T09:00:00Z"
```

## HITL Workflow

### Approve a Post

1. Review draft in `/In_Progress/linkedin-agent/`
2. If approved, **move file to `/Approved/`**
3. LinkedIn poster will automatically publish (within 2 minutes)

### Reject a Post

1. Review draft
2. If rejected, **move file to `/Rejected/`**
3. Add feedback in the file
4. Author can revise and resubmit

## Troubleshooting

### Gmail: No alerts appearing

1. Check credentials:
   ```bash
   python src/gmail/gmail_auth.py --test
   ```

2. Check if already processed:
   ```bash
   type Logs\processed_emails.json
   ```

3. Clear processed log (if needed):
   ```bash
   del Logs\processed_emails.json
   ```

### LinkedIn: Browser won't login

1. Poster runs in **headed mode** (visible browser)
2. First run: Manual login required
3. Subsequent runs: Uses saved session
4. If session expires, re-login automatically prompted

### LinkedIn: Post not publishing

1. Check HITL approval:
   - File MUST be in `/Approved/`
   - `hitl_approved` MUST be `true` in metadata

2. Check metadata:
   ```bash
   type Approved\your-post.md
   ```

3. Check audit log:
   ```bash
   type Logs\2026-03-28.json | findstr linkedin
   ```

### Triage: Wrong priority

1. Review triage rules:
   ```bash
   type config\triage_rules.yaml
   ```

2. Add missing keywords or VIP senders

3. Re-run Gmail monitor to re-process

## Integration Tests

Run all tests:
```bash
python tests/integration/test_phase2.py
```

Tests include:
- ✓ Gmail alert creation
- ✓ LinkedIn post detection
- ✓ Triage classification
- ✓ Audit logging

## File Structure

```
AI_Employee_vault/
├── src/
│   ├── gmail/
│   │   ├── gmail_monitor.py      # Main monitor script
│   │   ├── gmail_auth.py         # OAuth2 authentication
│   │   └── __main__.py           # Module entry point
│   ├── linkedin/
│   │   ├── linkedin_poster.py    # Main poster script
│   │   ├── post_generator.py     # Draft creation
│   │   ├── post_scheduler.py     # Scheduled posts
│   │   └── __main__.py           # Module entry point
│   ├── triage/
│   │   └── communication_triage.py  # Priority classification
│   └── config/
│       └── settings.py           # Configuration
├── config/
│   └── triage_rules.yaml         # Triage configuration
├── Briefings/
│   └── LinkedIn_Post_Template.md # Post template
├── Logs/
│   └── processed_emails.json     # Deduplication log
└── run_*.bat                     # Windows launchers
```

## Next Steps

### Phase 2 Completion Checklist

- [ ] Gmail monitor running continuously
- [ ] Email alerts appearing in `/Needs_Action`
- [ ] Triage rules configured for your use case
- [ ] LinkedIn poster tested with draft post
- [ ] HITL workflow understood and tested
- [ ] Audit logs being created

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
4. Run integration tests: `python tests/integration/test_phase2.py`
