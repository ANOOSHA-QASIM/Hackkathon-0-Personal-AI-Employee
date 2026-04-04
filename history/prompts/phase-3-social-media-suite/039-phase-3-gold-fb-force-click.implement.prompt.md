---
id: 039
title: phase-3-gold-fb-force-click
stage: implement
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-3-social-media-suite
branch: 003-phase-3-social-media-suite
user: Faiz
command: /sp.implement (phase-3-gold-fb-force-click)
labels: ["implementation", "phase-3", "javascript-click", "viewport-lock", "control-enter"]
links:
  spec: specs/003-phase-3-social-media-suite/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/skills/meta_poster.py (JS click + viewport lock + focus+type + Ctrl+Enter)
tests:
  - N/A (implementation - user must test Facebook)
---

## Prompt

/sp.implement { "phase": "phase-3-gold-fb-force-click", "instructions": [ "1. JAVASCRIPT CLICK: In 'meta_poster.py', instead of 'page.click()', use 'page.evaluate(\"() => { const buttons = Array.from(document.querySelectorAll('div[role=\\\"button\\\"]')); const postBtn = buttons.find(b => b.innerText.includes('What\\'s on your mind?')); if(postBtn) postBtn.click(); }\")'. This forces the modal to open via JS injection.", "2. VIEWPORT LOCK: Strictly set 'viewport': {'width': 1280, 'height': 720} to ensure the desktop layout is stable and the button is always in the same place.", "3. WAIT FOR MODAL: After the JS click, add 'page.wait_for_selector(\"div[role='textbox']\", timeout=15000)'. This ensures the AI waits for the dialog to fully pop up before typing.", "4. FOCUS & TYPE: Use 'page.focus(\"div[role='textbox']\")' and then 'page.keyboard.type(content, delay=100)'. The delay is crucial to trigger FB's internal 'is_typing' state.", "5. CONTROL+ENTER: Once typing is done, wait 3 seconds and then 'page.keyboard.press(\"Control+Enter\")' to publish without needing to find the 'Post' button." ] }

## Response snapshot

Implemented all Facebook force click requirements:

**Fixes Applied**:
1. ✓ JAVASCRIPT CLICK: JS injection to force modal open
   - page.evaluate("""() => {
       const buttons = Array.from(document.querySelectorAll('div[role="button"]'));
       const postBtn = buttons.find(b => b.innerText.includes("What's on your mind?") || b.innerText.includes("Write something..."));
       if(postBtn) { postBtn.click(); return true; }
       return false;
     }""")
   - Forces modal to open via JS injection
   - No reliance on page.click() which can fail

2. ✓ VIEWPORT LOCK: 1280x720 for stable desktop layout
   - viewport={'width': 1280, 'height': 720}
   - Button always in same place
   - Desktop layout guaranteed

3. ✓ WAIT FOR MODAL: Wait for textbox after JS click
   - page.wait_for_selector('div[role="textbox"]', timeout=15000)
   - Ensures modal fully popped up before typing
   - Extra 3s wait for modal animation

4. ✓ FOCUS & TYPE: Focus first, then type with 100ms delay
   - page.focus('div[role="textbox"]', timeout=120000)
   - page.wait_for_timeout(1000) - wait for focus to register
   - page.keyboard.type(content, delay=100) - triggers FB's 'is_typing' state

5. ✓ CONTROL+ENTER: Publish via keyboard shortcut
   - Wait 3 seconds after typing
   - page.keyboard.press('Control+Enter')
   - No need to find 'Post' button

**Exit Criteria**:
✅ The Facebook 'Create Post' modal opens automatically without the user clicking - IMPLEMENTED (JS injection)
✅ The text starts appearing in the box autonomously - IMPLEMENTED (focus+type with 100ms delay)
✅ The post is published via keyboard shortcut - IMPLEMENTED (Control+Enter)

**Files Updated**:
- src/skills/meta_poster.py (JS click + viewport lock + focus+type + Ctrl+Enter)

## Outcome

- ✅ Impact: Facebook posting now uses JS injection for maximum reliability
- 🧪 Tests: N/A (implementation - user must test Facebook)
- 📁 Files: 1 file updated with force click implementation
- 🔁 Next prompts: Run social_orchestrator.py --once to test Facebook
- 🧠 Reflection: JavaScript injection bypasses all UI interaction issues

## Evaluation notes (flywheel)

- Failure modes observed: None (force click implementation complete)
- Graders run and results: N/A (pending user to test)
- Prompt variant: Phase 3 Facebook force click
- Next experiment: Run orchestrator, verify modal opens via JS, text types autonomously, post publishes via Ctrl+Enter
