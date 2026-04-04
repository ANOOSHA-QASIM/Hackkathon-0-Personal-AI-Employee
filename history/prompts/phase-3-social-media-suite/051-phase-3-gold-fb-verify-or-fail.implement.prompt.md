---
id: 051
title: phase-3-gold-fb-verify-or-fail
stage: implement
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-3-social-media-suite
branch: 003-phase-3-social-media-suite
user: Faiz
command: /sp.implement (phase-3-gold-fb-verify-or-fail)
labels: ["implementation", "phase-3", "selector-fix", "visual-click", "wait-disappearance", "no-false-positives", "debug-screenshot"]
links:
  spec: specs/003-phase-3-social-media-suite/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/skills/meta_poster.py (precise textarea selectors + visual click + wait disappearance + no false positives + debug screenshot)
tests:
  - N/A (implementation - user must test Facebook)
---

## Prompt

/sp.implement { "phase": "phase-3-gold-fb-verify-or-fail", "instructions": [ "1. SELECTOR RE-FIX: In 'meta_poster.py', the sharer textarea is actually 'div[role=\"textbox\"]' or '#xm_0_1'. Find it precisely and use 'page.fill()' or 'page.type()'. Do not ignore the 'No textarea found' warning.", "2. VISUAL CLICK ONLY: Stop using 'Control+Enter' as it's unreliable. Use 'page.locator(\"button[type='submit']\").click({force: true, delay: 500})'. Before clicking, ensure the button is enabled (not grayed out).", "3. WAIT FOR DISAPPEARANCE: The script MUST wait for the window to close or the URL to change to 'facebook.com/dialog/return'. If the window is still open after 10 seconds, the post FAILED.", "4. NO FALSE POSITIVES: Change the success logic. Only log '✓ Facebook post published' if the 'Post to Facebook' button is no longer on the screen.", "5. DEBUG SCREENSHOT: If it fails, take a screenshot called 'E:\\hackathon_0_digital_fte\\AI_Employee_vault\\Logs\\sharer_fail.png' so we can see exactly what the AI is looking at." ] }

## Response snapshot

Implemented all Facebook verify-or-fail fixes:

**Fixes Applied**:
1. ✓ SELECTOR RE-FIX: Precise sharer textarea selectors
   - textarea_selectors = ['div[role="textbox"]', '#xm_0_1', 'textarea[name="message"]', 'textarea']
   - Try each selector until one works
   - Do not ignore 'No textarea found' warning

2. ✓ VISUAL CLICK ONLY: No more Control+Enter
   - submit_btn.click(force=True, delay=500, timeout=120000)
   - Check is_disabled before clicking
   - Only click if button is enabled (not grayed out)

3. ✓ WAIT FOR DISAPPEARANCE: 10 second timeout
   - for i in range(20):  # 20 x 500ms = 10 seconds
   - Check URL for 'facebook.com/dialog/return'
   - Check if Post button count == 0 (window closed)
   - If window still open after 10s = FAILED

4. ✓ NO FALSE POSITIVES: Strict success logic
   - Only return published if window_closed or url_changed
   - Check post_btn_count == 0 (button no longer on screen)
   - No more false 'Published' messages

5. ✓ DEBUG SCREENSHOT: On failure
   - error_screenshot_path = LOGS_PATH / 'sharer_fail.png'
   - page.screenshot(path=str(error_screenshot_path))
   - Shows exactly what AI was looking at

**Exit Criteria**:
✅ The AI correctly identifies the sharer textarea - IMPLEMENTED (4 precise selectors)
✅ The AI clicks the REAL blue button and waits for the window to close - IMPLEMENTED (visual click + 10s wait)
✅ No more 'False Published' messages in the terminal - IMPLEMENTED (strict success logic)

**Files Updated**:
- src/skills/meta_poster.py (precise textarea selectors + visual click + wait disappearance + no false positives + debug screenshot)

## Outcome

- ✅ Impact: Facebook posting now has strict verification - no false positives
- 🧪 Tests: N/A (implementation - user must test Facebook)
- 📁 Files: 1 file updated with verify-or-fail implementation
- 🔁 Next prompts: Run social_orchestrator.py --once to test verify-or-fail
- 🧠 Reflection: 10s wait + button disappearance check = no false positives

## Evaluation notes (flywheel)

- Failure modes observed: None (verify-or-fail implementation complete)
- Graders run and results: N/A (pending user to test)
- Prompt variant: Phase 3 Facebook verify-or-fail
- Next experiment: Run orchestrator, verify textarea found, button clicked, window closes in 10s, no false positives
