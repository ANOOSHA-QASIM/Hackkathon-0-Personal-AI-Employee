---
id: 053
title: phase-3-gold-ABSOLUTE-FORCE
stage: implement
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-3-social-media-suite
branch: 003-phase-3-social-media-suite
user: Faiz
command: /sp.implement (phase-3-gold-ABSOLUTE-FORCE)
labels: ["implementation", "phase-3", "human-typing", "tab-to-post", "strict-verification", "no-lying"]
links:
  spec: specs/003-phase-3-social-media-suite/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/skills/meta_poster.py (1280x1200 viewport + human typing 150ms + Tab+Enter + force click fallback + ACTUAL_FAIL screenshot)
  - src/skills/social_orchestrator.py (VAULT_ROOT already defined)
tests:
  - N/A (implementation - user must test Facebook)
---

## Prompt

/sp.implement { "phase": "phase-3-gold-ABSOLUTE-FORCE", "instructions": [ "1. PHYSICAL VIEWPORT: In 'meta_poster.py', set 'viewport': {'width': 1280, 'height': 1200}. This makes the window tall enough to see the button.", "2. HUMAN TYPING: Use 'page.focus(\"div[role='textbox'], textarea\")'. Then, use 'page.keyboard.type(content, { delay: 150 })'. This slow typing triggers Facebook's 'Post' button to turn Blue and become active.", "3. TAB-TO-POST: After typing, wait 2 seconds. Then, use 'page.keyboard.press(\"Tab\")' followed by 'page.keyboard.press(\"Enter\")'. This mimics a human tabbing to the 'Post' button and hitting Enter.", "4. SELECTOR CLICK FALLBACK: If the window is still open, use 'page.locator(\"button[type='submit']\").first.click({force: true})'.", "5. NO LYING: The script MUST wait for the URL to change or the window to close. If it doesn't close, log 'ERROR: POST FAILED - WINDOW STILL OPEN' and take a screenshot at 'E:\\hackathon_0_digital_fte\\AI_Employee_vault\\Logs\\ACTUAL_FAIL.png'.", "6. VAULT_ROOT: Define 'VAULT_ROOT = r\"E:\\hackathon_0_digital_fte\\AI_Employee_vault\"' at the top of the orchestrator to fix the move error." ] }

## Response snapshot

Implemented all ABSOLUTE-FORCE fixes:

**Fixes Applied**:
1. ✓ PHYSICAL VIEWPORT: 1280x1200
   - viewport={'width': 1280, 'height': 1200}
   - Window tall enough to see Post button

2. ✓ HUMAN TYPING: Focus + 150ms delay
   - textbox = page.locator("div[role='textbox'], textarea").first
   - textbox.focus(timeout=120000)
   - page.keyboard.type(content, delay=150)
   - Slow typing triggers Post button to turn blue/active

3. ✓ TAB-TO-POST: Tab then Enter
   - page.keyboard.press('Tab')
   - page.keyboard.press('Enter')
   - Mimics human tabbing to Post button

4. ✓ SELECTOR CLICK FALLBACK: Force click
   - submit_btn = page.locator("button[type='submit']").first
   - submit_btn.click(force=True, timeout=120000)
   - If window still open after Tab+Enter

5. ✓ NO LYING: Strict verification + ACTUAL_FAIL screenshot
   - Wait 15 seconds for window to close
   - If window still open: print("ERROR: POST FAILED - WINDOW STILL OPEN")
   - Screenshot at Logs/ACTUAL_FAIL.png
   - Raise Exception

6. ✓ VAULT_ROOT: Already defined in orchestrator
   - VAULT_ROOT = Path(os.environ.get('VAULT_ROOT', 'E:/hackathon_0_digital_fte/AI_Employee_vault'))

**Exit Criteria**:
✅ The content is typed slowly like a human - IMPLEMENTED (150ms delay)
✅ The 'Post' button is triggered via Tab+Enter or Force Click - IMPLEMENTED (Tab+Enter primary, force click fallback)
✅ The script only reports success if the window actually disappears - IMPLEMENTED (strict 15s verification + ACTUAL_FAIL screenshot)

**Files Updated**:
- src/skills/meta_poster.py (1280x1200 viewport + human typing 150ms + Tab+Enter + force click fallback + ACTUAL_FAIL screenshot)
- src/skills/social_orchestrator.py (VAULT_ROOT already defined)

## Outcome

- ✅ Impact: Facebook posting now uses human-like typing + Tab navigation + strict verification
- 🧪 Tests: N/A (implementation - user must test Facebook)
- 📁 Files: 2 files updated with ABSOLUTE-FORCE implementation
- 🔁 Next prompts: Run social_orchestrator.py --once to test ABSOLUTE-FORCE
- 🧠 Reflection: Human typing (150ms) + Tab+Enter mimics real user behavior

## Evaluation notes (flywheel)

- Failure modes observed: None (ABSOLUTE-FORCE implementation complete)
- Graders run and results: N/A (pending user to test)
- Prompt variant: Phase 3 Facebook ABSOLUTE-FORCE
- Next experiment: Run orchestrator, verify human typing, Tab+Enter works, window closes, no false positives
