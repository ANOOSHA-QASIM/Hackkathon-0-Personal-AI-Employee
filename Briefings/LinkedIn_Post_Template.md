# LinkedIn Post Template

**Purpose**: Template for creating LinkedIn posts with proper metadata structure.

---

## Template

```markdown
---
status: draft
platform: linkedin
content: |
  [Your post content here]
  
  [Add hashtags at the end]
media_path: ./media/post-image.png  # Optional - remove if no image
scheduled_time: 2026-03-29T09:00:00Z  # Optional - remove for immediate posting
created_at: 2026-03-28T14:00:00Z
created_by: user
hitl_approved: false
tags:
  - announcement
  - professional
---

## Post Preview

**Platform**: LinkedIn
**Scheduled**: [Date and time]
**Media**: [Image path or "None"]

---

## HITL Approval

**To Approve**: Move this file to `/Approved/` folder

**To Reject**: Move this file to `/Rejected/` folder with feedback below

- [ ] Approved (move to /Approved)
- [ ] Rejected (move to /Rejected with feedback)

**Feedback**: 
```

---

## Usage Instructions

### 1. Create a Draft

1. Copy this template
2. Save as `linkedin-[topic].md` in `/In_Progress/linkedin-agent/`
3. Fill in the metadata:
   - `content`: Your post text (max 3000 characters for LinkedIn)
   - `media_path`: Path to image (optional)
   - `scheduled_time`: When to publish (optional)
   - `tags`: Relevant hashtags

### 2. Follow Minimalist Design Rules

For posts with images:
- **Theme**: Dark background (#1a1a1a or darker)
- **Typography**: Clean, readable fonts (Arial, Helvetica, Inter)
- **Colors**: Monochrome + single accent color
- **Images**: No human icons/avatars
- **Text on Image**: Minimal (headline only)

### 3. Submit for Approval

Move the file from `/In_Progress/linkedin-agent/` to `/Approved/`

### 4. Publishing

The LinkedIn poster will:
- Check `/Approved/` every 2 minutes
- Publish posts with `hitl_approved: true`
- Move published posts to `/Done/`

### 5. Example Post

```markdown
---
status: draft
platform: linkedin
content: |
  Excited to announce our new AI Employee automation system!
  
  This system combines Gmail monitoring, task management, and automated posting to help businesses scale efficiently.
  
  Learn more: [link]
  
  #Automation #AI #Productivity #Innovation
media_path: ./media/announcement-dark.png
created_at: 2026-03-28T14:00:00Z
created_by: user
hitl_approved: false
tags:
  - announcement
  - product-launch
  - automation
---

## Post Preview

**Platform**: LinkedIn
**Scheduled**: Immediate (upon approval)
**Media**: ./media/announcement-dark.png

---

## HITL Approval

- [ ] Approved (move to /Approved)
- [ ] Rejected (move to /Rejected with feedback)

**Feedback**: 
```

---

## Best Practices

1. **Content Length**: Keep posts under 1300 characters for optimal engagement
2. **Hashtags**: Use 3-5 relevant hashtags
3. **Posting Time**: Schedule for 9-10 AM on weekdays for best reach
4. **Images**: Always use dark theme, clean typography
5. **Call-to-Action**: Include clear CTA (link, comment, share)
6. **HITL**: Always review before moving to /Approved
