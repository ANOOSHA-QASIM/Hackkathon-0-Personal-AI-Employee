# Business Dashboard

**Last Updated**: 2026-03-28  
**Phase**: 1 (Foundation) - Manual Entry

---

## 📊 Bank Balance

> **Note**: Phase 1 - Manual entry. Phase 2+ will automate from bank API.

- **Current Balance**: $X,XXX.XX USD
- **Last Updated**: 2026-03-28
- **Last Transaction**: YYYY-MM-DD (Description - $Amount)

---

## 📬 Pending Messages

> **Note**: Phase 1 - Manual count. Phase 2+ will auto-count from Gmail/WhatsApp.

- **Gmail**: 0 unread
- **WhatsApp**: 0 unread
- **Last Checked**: 2026-03-28

---

## 🏗️ Active Projects

| Project | Status | Next Action | Last Updated |
|---------|--------|-------------|--------------|
| [Add Project] | Waiting | Define first task | 2026-03-28 |

### Status Definitions

- **In_Progress**: Actively being worked on
- **Waiting**: Waiting on external party (client, vendor, etc.)
- **Blocked**: Cannot proceed due to obstacle

---

## 📧 Communication Hub

> **Note**: Phase 2 - Auto-populated by Gmail Watcher and LinkedIn Poster.

### Recent Email Alerts (from /Needs_Action)

| Date | Sender | Subject | Priority | Status |
|------|--------|---------|----------|--------|
| [Auto-populated] | [Sender] | [Subject] | [High/Normal/Low] | [Needs_Action] |

**How to view**: Check `/Needs_Action/email-*.md` files for email alerts.

### Social Media Queue

| Post | Platform | Status | Scheduled | Approved |
|------|----------|--------|-----------|----------|
| [Post Title] | LinkedIn | [Draft/Approved/Posted] | [Time] | [Yes/No] |

**How to view**:
- Drafts: `/In_Progress/linkedin-agent/*.md`
- Approved (pending): `/Approved/*.md`
- Posted: `/Done/*.md`

---

## Quick Links

- [Dashboard.md](./Dashboard.md) - This file
- [Company_Handbook.md](./Company_Handbook.md) - AI rules and guidelines
- [/Inbox](./Inbox/) - Drop files here for processing
- [/Needs_Action](./Needs_Action/) - Pending tasks (including email alerts)
- [/In_Progress](./In_Progress/) - Active tasks
- [/Approved](./Approved/) - Awaiting human approval (including LinkedIn posts)
- [/Done](./Done/) - Completed tasks
- [/Logs](./Logs/) - Audit logs
- [LinkedIn_Post_Template.md](./Briefings/LinkedIn_Post_Template.md) - Template for creating posts

---

## Phase 2+ Roadmap

### Planned Automations

- [ ] **Bank Balance**: Auto-fetch from Odoo/bank API
- [ ] **Pending Messages**: Auto-count from Gmail/WhatsApp watchers
- [ ] **Active Projects**: Auto-populate from `/In_Progress` folder metadata
- [ ] **Refresh Rate**: Auto-update every 5 minutes
