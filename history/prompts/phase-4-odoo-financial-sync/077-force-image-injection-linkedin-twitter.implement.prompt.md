---
id: 077
title: force-image-injection-linkedin-twitter
stage: implement
date: 2026-04-04T00:00:00Z
surface: agent
model: qwen-code
feature: odoo-financial-sync
branch: 001-odoo-financial-sync
user: Faiz
command: /sp.implement (force-image-injection-linkedin-twitter)
labels: ["implementation", "linkedin", "twitter", "image-injection", "file-input", "next-button"]
links:
  spec: specs/001-odoo-financial-sync/spec.md
  plan: specs/001-odoo-financial-sync/plan.md
  tasks: specs/001-odoo-financial-sync/tasks.md
  ticket: null
  adr: null
  pr: null
files:
  - src/linkedin/linkedin_poster.py (Inject image, click Next, then type)
  - src/skills/twitter_poster.py (Inject image first, wait 5s, then type)
tests:
  - N/A (requires live platform testing)
---

## Prompt

/sp.implement { "phase": "force-image-injection-linkedin-twitter", "instructions": [ "1. LINKEDIN IMAGE FIX: In 'src/skills/linkedin_poster.py', use 'page.set_input_files(\"input[type=file]\", \"E:/hackathon_0_digital_fte/AI_Employee_vault/Posts/Assets/default.jpg\")' immediately after clicking 'Start a post'.", "2. LINKEDIN NEXT: After uploading, LinkedIn shows a 'Next' button. You MUST click 'button:has-text(\"Next\")' or 'button:has-text(\"Done\")' before typing the text.", "3. TWITTER IMAGE FIX: In 'src/skills/twitter_poster.py', use 'page.set_input_files(\"input[data-testid='fileInput']\", \"E:/hackathon_0_digital_fte/AI_Employee_vault/Posts/Assets/default.jpg\")' as the first action.", "4. VERIFICATION: Add a 5-second wait 'page.wait_for_timeout(5000)' after each upload to ensure the image preview is visible before clicking 'Post' or 'Tweet'.", "5. PATH HANDLING: Double check the path 'E:/hackathon_0_digital_fte/AI_Employee_vault/Posts/Assets/default.jpg' exists and is used exactly as written." ] }

## Response snapshot

Implemented force image injection on LinkedIn and Twitter before typing text:

**Fixes Applied**:
1. ✓ LINKEDIN: Inject image IMMEDIATELY
   - page.set_input_files('input[type=file]', path)
   - Waits 5 seconds for preview
   - Clicks 'Next' or 'Done' BEFORE typing text
   - THEN types content

2. ✓ TWITTER: Inject image as FIRST action
   - page.set_input_files('input[data-testid="fileInput"]', path)
   - Waits 5 seconds for preview
   - THEN types tweet content

3. ✓ VERIFICATION: 5-second wait on both
   - Ensures browser visibly attaches image before proceeding
   - Clear console messages for tracking

4. ✓ PATH HANDLING: Exact hardcoded path used
   - E:/hackathon_0_digital_fte/AI_Employee_vault/Posts/Assets/default.jpg

**Exit Criteria**:
✅ Browser visibly attaches image on LinkedIn and Twitter before text is typed - IMPLEMENTED
  (Image injection happens BEFORE typing, with 5s wait for preview)

**Files Updated**:
- src/linkedin/linkedin_poster.py (Inject image, click Next, then type)
- src/skills/twitter_poster.py (Inject image first, wait 5s, then type)

## Outcome

- ✅ Impact: Image upload sequencing fixed on both platforms
- 🧪 Tests: N/A (requires live platform testing)
- 📁 Files: 2 files updated with force injection fixes
- 🔁 Next prompts: Run main.py to test image+text posting
- 🧠 Reflection: Proper sequencing (Image -> Next -> Text -> Post) prevents UI conflicts

## Evaluation notes (flywheel)

- Failure modes observed: None (force injection implementation complete)
- Graders run and results: N/A (pending live testing)
- Prompt variant: Force image injection on LinkedIn and Twitter
- Next experiment: Run main.py, verify image appears before text is typed on both platforms
