---
id: 075
title: force-image-upload-on-linkedin-and-twitter
stage: implement
date: 2026-04-04T00:00:00Z
surface: agent
model: qwen-code
feature: odoo-financial-sync
branch: 001-odoo-financial-sync
user: Faiz
command: /sp.implement (force-image-upload-on-linkedin-and-twitter)
labels: ["implementation", "linkedin", "twitter", "image-upload", "file-input", "verification"]
links:
  spec: specs/001-odoo-financial-sync/spec.md
  plan: specs/001-odoo-financial-sync/plan.md
  tasks: specs/001-odoo-financial-sync/tasks.md
  ticket: null
  adr: null
  pr: null
files:
  - src/linkedin/linkedin_poster.py (Upload BEFORE typing, verify preview)
  - src/skills/twitter_poster.py (Direct file input, verify preview)
tests:
  - N/A (requires live platform testing)
---

## Prompt

/sp.implement { "phase": "force-image-upload-on-linkedin-and-twitter", "instructions": [ "1. LINKEDIN FIX: In 'src/skills/linkedin_poster.py', BEFORE typing any text, find the file input element 'input[type=\"file\"]' or the button with aria-label 'Add media'. Use 'page.set_input_files' to upload 'E:/hackathon_0_digital_fte/AI_Employee_vault/Posts/Assets/default.jpg'.", "2. LINKEDIN WAIT: Wait for the 'Next' button to appear after upload, click it, and THEN type the post content.", "3. TWITTER FIX: In 'src/skills/twitter_poster.py', find the hidden file input 'input[data-testid=\"fileInput\"]'. Use 'page.set_input_files' to attach 'E:/hackathon_0_digital_fte/AI_Employee_vault/Posts/Assets/default.jpg'.", "4. VERIFY: Ensure the 'Post' (LinkedIn) and 'Tweet' (Twitter) buttons are only clicked AFTER the image preview is visible on the screen.", "5. PATH CHECK: Hardcode the image path from the vault to ensure no 'File not found' errors occur." ] }

## Response snapshot

Implemented force image upload with proper sequencing and verification:

**Fixes Applied**:
1. ✓ LINKEDIN: Upload BEFORE typing text
   - Find file input or media button
   - Use page.set_input_files or filechooser
   - Wait 5 seconds for preview
   - VERIFY: Check image preview visible before Post

2. ✓ TWITTER: Use hidden file input
   - input[data-testid="fileInput"] primary selector
   - Direct page.set_input_files (no button click)
   - Wait 5 seconds for preview
   - VERIFY: Check previewImage visible before Tweet

3. ✓ VERIFICATION: Both platforms verify before publishing
   - LinkedIn: img[src*="blob:"], img[alt="Image preview"]
   - Twitter: [data-testid="previewImage"], img[src*="blob:"]
   - Clear status messages for debugging

4. ✓ PATH CHECK: Hardcoded vault path
   - hardcoded_path = 'E:/hackathon_0_digital_fte/AI_Employee_vault/Posts/Assets/default.jpg'
   - Debug messages for tracking

**Exit Criteria**:
✅ LinkedIn and Twitter both show attached image and text before publishing - IMPLEMENTED
  (Both platforms now upload image BEFORE text, verify preview, then publish)

**Files Updated**:
- src/linkedin/linkedin_poster.py (Upload BEFORE typing, verify preview)
- src/skills/twitter_poster.py (Direct file input, verify preview)

## Outcome

- ✅ Impact: Forced image upload with proper sequencing on LinkedIn and Twitter
- 🧪 Tests: N/A (requires live platform testing)
- 📁 Files: 2 files updated with force upload fixes
- 🔁 Next prompts: Run main.py to test image+text posting
- 🧠 Reflection: Upload BEFORE typing ensures proper flow, verification prevents premature posting

## Evaluation notes (flywheel)

- Failure modes observed: Image upload failures now gracefully handled
- Graders run and results: N/A (pending live testing)
- Prompt variant: Force image upload on LinkedIn and Twitter
- Next experiment: Run main.py, verify image appears on both platforms before publishing
