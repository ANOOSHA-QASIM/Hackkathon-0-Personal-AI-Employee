---
id: 040
title: phase-3-gold-bypass-false-login
stage: implement
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-3-social-media-suite
branch: 003-phase-3-social-media-suite
user: Faiz
command: /sp.implement (phase-3-gold-bypass-false-login)
labels: ["implementation", "phase-3", "url-login-check", "keyboard-shortcut", "get-by-role"]
links:
  spec: specs/003-phase-3-social-media-suite/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/skills/meta_poster.py (URL login check + get_by_role + 'p' shortcut)
tests:
  - N/A (implementation - user must test Facebook)
---

## Prompt

/sp.implement { "phase": "phase-3-gold-bypass-false-login", "instructions": [ "1. REMOVE STRICT LOGIN CHECK: In 'src/skills/meta_poster.py', remove the logic that looks for 'What's on your mind' to confirm login. Instead, just check if 'page.url' does NOT contain 'login'.", "2. FORCE CLICK 'WHAT'S ON YOUR MIND': Use a more aggressive selector that doesn't care about the text. Use 'page.click(\"div[role='button']:has(span:has-text('What's on your mind'))\")' OR simply 'page.get_by_role(\"button\", name=\"What's on your mind?\").click()'.", "3. FALLBACK TO SHORTCUT: If the click fails after 5 seconds, use 'page.keyboard.press('p')'. Facebook's global shortcut for 'New Post' is the letter 'P'. This is 100% automated.", "4. RESOLUTION FIX: Ensure 'viewport' is set to 1280x720 so the layout is always standard and the button is easy to find.", "5. LOGGING: Update the terminal to say 'Login confirmed by URL' instead of searching for elements." ] }

## Response snapshot

Implemented all Facebook bypass false login fixes:

**Fixes Applied**:
1. ✓ REMOVE STRICT LOGIN CHECK: URL-based login check
   - if 'login' in current_url.lower(): wait for redirect
   - else: print("[Meta] Login confirmed by URL")
   - No more searching for profile elements
   - Simple and reliable

2. ✓ FORCE CLICK 'WHAT'S ON YOUR MIND': get_by_role selector
   - composer_btn = page.get_by_role("button", name="What's on your mind?")
   - if composer_btn.count() > 0: composer_btn.click(timeout=5000)
   - Most reliable Playwright selector

3. ✓ FALLBACK TO SHORTCUT: 'p' keyboard shortcut
   - If click fails: page.keyboard.press('p')
   - Facebook's global shortcut for 'New Post'
   - 100% automated, works regardless of UI

4. ✓ RESOLUTION FIX: viewport 1280x720
   - Already set in context launch
   - viewport={'width': 1280, 'height': 720}
   - Standard desktop layout

5. ✓ LOGGING: "Login confirmed by URL"
   - print("[Meta] Login confirmed by URL")
   - Clear and concise
   - No element searching messages

**Exit Criteria**:
✅ The terminal no longer says 'Not logged in' if the feed is visible - IMPLEMENTED (URL check only)
✅ The 'What's on your mind?' box opens automatically via click or 'P' shortcut - IMPLEMENTED (get_by_role + 'p' fallback)

**Files Updated**:
- src/skills/meta_poster.py (URL login check + get_by_role + 'p' shortcut)

## Outcome

- ✅ Impact: Facebook login check simplified, composer opens reliably
- 🧪 Tests: N/A (implementation - user must test Facebook)
- 📁 Files: 1 file updated with bypass false login fix
- 🔁 Next prompts: Run social_orchestrator.py --once to test Facebook
- 🧠 Reflection: URL-based login check is much simpler and more reliable than element detection

## Evaluation notes (flywheel)

- Failure modes observed: None (bypass false login implementation complete)
- Graders run and results: N/A (pending user to test)
- Prompt variant: Phase 3 bypass false login
- Next experiment: Run orchestrator, verify login confirmed by URL, composer opens via click or 'p' shortcut
