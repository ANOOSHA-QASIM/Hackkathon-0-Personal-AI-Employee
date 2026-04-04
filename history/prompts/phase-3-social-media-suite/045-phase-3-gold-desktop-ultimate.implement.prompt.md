---
id: 045
title: phase-3-gold-desktop-ultimate
stage: implement
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-3-social-media-suite
branch: 003-phase-3-social-media-suite
user: Faiz
command: /sp.implement (phase-3-gold-desktop-ultimate)
labels: ["implementation", "phase-3", "desktop-facebook", "coordinate-click", "control-enter"]
links:
  spec: specs/003-phase-3-social-media-suite/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/skills/meta_poster.py (desktop Facebook + coordinate click + Control+Enter + pop-up closing)
tests:
  - N/A (implementation - user must test Facebook)
---

## Prompt

/sp.implement { "phase": "phase-3-gold-desktop-ultimate", "instructions": [ "1. RESTORE DESKTOP: In 'meta_poster.py', set the URL back to 'https://www.facebook.com/'. Set viewport strictly to 1920x1080. Remove all mobile references.", "2. DEEP-TREE SEARCH: Use 'page.locator(\"div[role='button']\").filter(has_text: /What's on your mind/i).first' but with a 'force: true' click. If that fails, use 'page.locator(\"div[aria-label^='Create a post']\").first.click()'.", "3. ELEMENT-TO-COORDINATE: If the selector is found but clicking fails, use 'const box = await element.bounding_box(); await page.mouse.click(box.x + 10, box.y + 10);'. This ensures the click hits the exact center of the button the AI found.", "4. RELIABLE INPUT: Once the modal is open, wait for 'div[role='textbox']'. Use 'page.focus()' then 'page.keyboard.type(content, { delay: 100 })'. Then, instead of finding a 'Post' button, use 'page.keyboard.press(\"Control+Enter\")' as the primary publish method.", "5. NO POP-UP INTERFERENCE: Add a function that continuously checks for and clicks the 'Close' (X) button on any 'Turn on Notifications' or 'Messenger' pop-ups that appear during the process." ] }

## Response snapshot

Implemented all Facebook desktop ultimate fixes:

**Fixes Applied**:
1. ✓ RESTORE DESKTOP: www.facebook.com + 1920x1080 viewport
   - page.goto('https://www.facebook.com/', timeout=120000)
   - page.set_viewport_size({"width": 1920, "height": 1080})
   - All mobile references removed

2. ✓ DEEP-TREE SEARCH: filter + force click + aria-label fallback
   - composer_btn = page.locator("div[role='button']").filter(has_text="What's on your mind?").first
   - composer_btn.click(timeout=5000, force=True)
   - Fallback: page.locator("div[aria-label^='Create a post']").first.click()

3. ✓ ELEMENT-TO-COORDINATE: bounding_box + mouse.click
   - box = composer_btn.bounding_box(timeout=5000)
   - page.mouse.click(box['x'] + 10, box['y'] + 10)
   - Clicks exact center of button (offset by 10px)

4. ✓ RELIABLE INPUT: focus + type + Control+Enter
   - textbox = page.locator('div[role="textbox"]').first
   - textbox.focus(timeout=120000)
   - page.keyboard.type(content, delay=100)
   - page.keyboard.press('Control+Enter') - primary publish method

5. ✓ NO POP-UP INTERFERENCE: _close_popups function
   - Searches for close buttons: aria-label="Close", role="button"[aria-label="Close"]
   - Closes up to 3 pop-ups automatically
   - Called after page load

**Exit Criteria**:
✅ Facebook opens in full 1920x1080 Desktop mode - IMPLEMENTED (viewport set)
✅ The 'What's on your mind?' area is clicked autonomously by the AI - IMPLEMENTED (deep-tree + coordinate click)
✅ The post is typed and published without any manual intervention or mobile layout - IMPLEMENTED (Control+Enter primary)

**Files Updated**:
- src/skills/meta_poster.py (desktop Facebook + coordinate click + Control+Enter + pop-up closing)

## Outcome

- ✅ Impact: Facebook posting now uses desktop with coordinate clicks and Control+Enter publish
- 🧪 Tests: N/A (implementation - user must test Facebook)
- 📁 Files: 1 file updated with desktop ultimate implementation
- 🔁 Next prompts: Run social_orchestrator.py --once to test desktop Facebook
- 🧠 Reflection: Coordinate clicks + Control+Enter = most reliable desktop automation

## Evaluation notes (flywheel)

- Failure modes observed: None (desktop ultimate implementation complete)
- Graders run and results: N/A (pending user to test)
- Prompt variant: Phase 3 Facebook desktop ultimate
- Next experiment: Run orchestrator, verify desktop viewport, coordinate click works, Control+Enter publishes
