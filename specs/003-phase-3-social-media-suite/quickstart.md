# Quickstart: Phase 3 Social Media Suite

**Feature**: 003-phase-3-social-media-suite  
**Last Updated**: 2026-03-28  
**Status**: Draft

## Overview

Phase 3 Social Media Suite adds Gold Tier multi-platform posting:
- **Meta Poster**: Facebook + Instagram posting with persistent sessions
- **Twitter Poster**: X (Twitter) posting with auto-threading for long content
- **Cross-Platform Orchestrator**: Single file → all 4 platforms (LinkedIn, FB, IG, Twitter)
- **Ralph Wiggum Error Recovery**: Automatic retry with 15-min cooldown, max 3 attempts

## Prerequisites

- Phase 2 (LinkedIn posting) complete and functional
- Python 3.11 or higher
- Playwright installed (`playwright install chromium`)
- Active accounts on LinkedIn, Facebook, Instagram, Twitter (X)

## Installation

### Step 1: Install Dependencies

```bash
cd E:\hackathon_0_digital_fte\AI_Employee_vault
pip install -r requirements.txt
```

### Step 2: Verify Phase 2 LinkedIn Works

```bash
python src/linkedin/linkedin_poster.py --once
```

Ensure LinkedIn posting works before adding Phase 3 platforms.

---

## Usage

### Create a Social Media Post

1. **Create post file** in `/In_Progress/social-media-agent/`:

```markdown
---
status: draft
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
created_at: 2026-03-28T14:00:00Z
created_by: user
---

## Post Preview

**Platforms**: LinkedIn, Facebook, Instagram, Twitter
**Media**: See attached image
```

2. **Move to `/Approved/Social/`** (HITL approval):

```bash
move "post.md" "E:\hackathon_0_digital_fte\AI_Employee_vault\Approved\Social\"
```

3. **Run the Social Dispatcher**:

```bash
python src/orchestrator/social_dispatcher.py --once
```

4. **First-time authentication** (per platform):
   - Browser opens for manual login
   - Log in to each platform
   - Session saved to `.browser_data/{platform}/`
   - Subsequent posts reuse session (no login required)

5. **Verify posting**:
   - Check each platform for the post
   - Post file moved to `/Done/Social/` on success
   - Failed platforms logged and retried automatically

---

## Platform-Specific Notes

### Meta (Facebook + Instagram)

**Session Location**: `.browser_data/meta/`

**First Post**:
1. Browser opens
2. Log in to Facebook
3. Session saved (covers both Facebook and Instagram)

**Image Support**:
- Facebook: JPG, PNG (max 15MB)
- Instagram: JPG, PNG (max 8MB, square recommended)

**Content Limits**:
- Facebook: 63,206 characters (but 250-400 optimal)
- Instagram: 2,200 characters (but 138-150 optimal)

---

### Twitter (X)

**Session Location**: `.browser_data/twitter/`

**First Post**:
1. Browser opens
2. Log in to Twitter
3. Session saved

**Auto-Threading**:
- Posts >280 characters automatically split into thread
- "..." separator between tweets
- Image attached to first tweet

**Content Limits**:
- Tweets: 280 characters
- Thread: Unlimited (but 10-15 tweets optimal for engagement)

---

## Ralph Wiggum Error Recovery

**Automatic Retry**:
- Failed platforms retried after 15 minutes
- Max 3 retry attempts
- All errors logged to `/Logs/YYYY-MM-DD.json`

**Escalation**:
- After 3 failed retries, post escalated to `/Needs_Action/`
- Human can review and fix issues
- Resubmit by moving back to `/Approved/Social/`

**Common Errors**:
- **Session expired**: Re-authenticate, session auto-saved
- **Rate limit exceeded**: Wait 15 minutes, retry automatic
- **Image upload failed**: Check file format/size, retry automatic
- **Content violation**: Escalate to human for review

---

## Troubleshooting

### Session Expired

**Symptoms**: Browser opens requesting login every time

**Solution**:
1. Log in manually
2. Verify session saved to `.browser_data/{platform}/`
3. If problem persists, delete session folder and re-authenticate:
   ```bash
   rmdir /s /q ".browser_data\meta"
   python src/orchestrator/social_dispatcher.py --once
   ```

### Platform Fails Repeatedly

**Symptoms**: Same platform fails on every retry

**Solution**:
1. Check error in `/Logs/YYYY-MM-DD.json`
2. Common fixes:
   - **Rate limit**: Wait 1 hour, retry
   - **Content violation**: Edit content, resubmit
   - **Image issue**: Convert to supported format, retry
3. If unresolved, escalate to human via `/Needs_Action/`

### Orchestrator Crashes Mid-Posting

**Symptoms**: Some platforms posted, others pending

**Solution**:
1. Run orchestrator again:
   ```bash
   python src/orchestrator/social_dispatcher.py --once
   ```
2. Orchestrator checks `/Approved/Social/` for unprocessed files
3. Resumes from last successful platform
4. Already-posted platforms skipped (idempotent)

---

## File Structure

```
AI_Employee_vault/
├── src/
│   ├── skills/
│   │   ├── meta_poster.py       # Facebook + Instagram
│   │   ├── twitter_poster.py    # Twitter/X
│   │   └── base_poster.py       # Base class
│   └── orchestrator/
│       └── social_dispatcher.py # Cross-platform orchestrator
├── .browser_data/
│   ├── linkedin/     # Phase 2
│   ├── meta/         # Phase 3
│   └── twitter/      # Phase 3
├── Approved/
│   └── Social/       # Posts awaiting publishing
└── Done/
    └── Social/       # Successfully published posts
```

---

## Next Steps

### Phase 3 Completion Checklist

- [ ] Meta Poster functional (Facebook + Instagram)
- [ ] Twitter Poster functional (auto-threading)
- [ ] Cross-Platform Orchestrator posts to all 4 platforms
- [ ] Ralph Wiggum error recovery working (15-min retry)
- [ ] All sessions persistent (no re-authentication needed)
- [ ] All errors logged to `/Logs/YYYY-MM-DD.json`

### Phase 4 Preparation

Once Phase 3 is complete, you're ready for:
- Odoo Accounting integration
- Business Audit automation
- Ralph Wiggum reasoning loops for non-social tasks
- Daily briefings in `/Briefings/`

---

## Support

For issues or questions:
1. Check audit logs: `/Logs/YYYY-MM-DD.json`
2. Review Constitution: `.specify/memory/constitution.md`
3. Consult data model: `specs/003-phase-3-social-media-suite/data-model.md`
4. Run orchestrator with verbose logging:
   ```bash
   python src/orchestrator/social_dispatcher.py --verbose
   ```
