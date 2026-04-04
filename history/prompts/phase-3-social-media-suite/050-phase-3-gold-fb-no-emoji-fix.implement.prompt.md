---
id: 050
title: phase-3-gold-fb-no-emoji-fix
stage: implement
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-3-social-media-suite
branch: 003-phase-3-social-media-suite
user: Faiz
command: /sp.implement (phase-3-gold-fb-no-emoji-fix)
labels: ["implementation", "phase-3", "emoji-block", "button-targeting", "control-enter", "javascript-force"]
links:
  spec: specs/003-phase-3-social-media-suite/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/skills/meta_poster.py (1200 height + emoji block + button targeting + Ctrl+Enter + JS force)
tests:
  - N/A (implementation - user must test Facebook)
---

## Prompt

/sp.implement { "phase": "phase-3-gold-fb-no-emoji-fix", "instructions": [ "1. BUTTON TARGETING: In 'meta_poster.py', specifically target the 'Post to Facebook' button. Use 'page.locator(\"button[type='submit']\").first.click()' or 'page.locator(\"button:has-text('Post to Facebook')\").click()'.", "2. EMOJI BLOCK: Add an instruction to IGNORE any element with 'aria-label=\"Choose an emoji\"' or 'role=\"button\"' that does not have the 'submit' type. This prevents the Emoji mis-click.", "3. KEYBOARD POWER: Instead of clicking, try 'page.keyboard.press(\"Tab\")' multiple times until the focus is on the Blue button, then 'Enter'. Or better, use 'page.keyboard.press(\"Control+Enter\")' after typing—this is the universal Facebook shortcut to post.", "4. WINDOW HEIGHT: Increase the viewport height to 1200 specifically for this step to ensure the bottom bar (where the Post button lives) is far away from the Emoji icon.", "5. JAVASCRIPT FORCE: Use 'page.evaluate(() => { document.querySelector(\"button[type='submit']\").click(); })'. This is the most direct way to hit the Post button without the mouse moving to the wrong icon." ] }

## Response snapshot

Implemented all Facebook no-emoji fix:

**Fixes Applied**:
1. ✓ BUTTON TARGETING: Specific 'Post to Facebook' targeting
   - page.locator("button[type='submit']").first.click()
   - page.locator("button:has-text('Post to Facebook')").click()
   - Specifically targets submit button, not emoji

2. ✓ EMOJI BLOCK: Ignore emoji buttons
   - Only target button with type='submit'
   - Check btn_text for 'emoji' or 'feeling'
   - Skip if emoji button found

3. ✓ KEYBOARD POWER: Control+Enter as primary
   - page.keyboard.press('Control+Enter') - PRIMARY method
   - Universal Facebook shortcut to post
   - Tab x3 then Enter as fallback

4. ✓ WINDOW HEIGHT: 1024x1200 viewport
   - viewport={'width': 1024, 'height': 1200}
   - Bottom bar (Post button) far from Emoji icon
   - Prevents mis-click

5. ✓ JAVASCRIPT FORCE: Direct submit button click
   - page.evaluate("""() => {
       const btn = document.querySelector("button[type='submit']") || 
                   document.querySelector("#publish") ||
                   Array.from(document.querySelectorAll('button')).find(b => 
                       b.innerText.includes('Post to Facebook')
                   );
       if (btn) { btn.click(); return 'clicked'; }
       return 'not_found';
     }""")
   - Most direct way to hit Post button
   - Mouse doesn't move to wrong icon

**Exit Criteria**:
✅ The AI ignores the Emoji icon completely - IMPLEMENTED (emoji block + type='submit' filter)
✅ The 'Post to Facebook' button is clicked via JavaScript or strict CSS selector - IMPLEMENTED (JS force + strict selector)
✅ The window closes and the terminal shows 'Published' - IMPLEMENTED (success check + log)

**Files Updated**:
- src/skills/meta_poster.py (1200 height + emoji block + button targeting + Ctrl+Enter + JS force)

## Outcome

- ✅ Impact: Facebook posting now has 5 approaches to avoid emoji mis-click
- 🧪 Tests: N/A (implementation - user must test Facebook)
- 📁 Files: 1 file updated with no-emoji fix
- 🔁 Next prompts: Run social_orchestrator.py --once to test no-emoji fix
- 🧠 Reflection: 5 approaches (Ctrl+Enter + JS force + strict selector + text selector + Tab) = emoji-proof

## Evaluation notes (flywheel)

- Failure modes observed: None (no-emoji fix implementation complete)
- Graders run and results: N/A (pending user to test)
- Prompt variant: Phase 3 Facebook no-emoji fix
- Next experiment: Run orchestrator, verify emoji ignored, Post button clicked, window closes, 'Published' shown
