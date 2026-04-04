---
id: 052
title: phase-3-gold-TITAN-FINAL
stage: implement
date: 2026-03-28T00:00:00Z
surface: agent
model: qwen-code
feature: phase-3-social-media-suite
branch: 003-phase-3-social-media-suite
user: Faiz
command: /sp.implement (phase-3-gold-TITAN-FINAL)
labels: ["implementation", "phase-3", "javascript-only", "verification-lock", "auto-file-move", "strict-failure"]
links:
  spec: specs/003-phase-3-social-media-suite/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - src/skills/meta_poster.py (1920x1200 viewport + JS-only submission + 15s verification + auto file move)
  - src/skills/social_orchestrator.py (pass post_file_path to meta_poster)
tests:
  - N/A (implementation - user must test Facebook)
---

## Prompt

/sp.implement { "phase": "phase-3-gold-TITAN-FINAL", "instructions": [ "1. ABSOLUTE VIEWPORT: In 'meta_poster.py', set 'viewport': {'width': 1920, 'height': 1200}. This ensures the 'Post' button is always within the DOM's reachable area.", "2. JAVASCRIPT-ONLY SUBMISSION: Instead of searching for buttons to click, use 'page.evaluate((text) => { const box = document.querySelector(\"div[role='textbox'], textarea#xm_0_1, [contenteditable='true']\"); if(box) { if(box.tagName === 'TEXTAREA') box.value = text; else box.innerText = text; box.dispatchEvent(new Event('input', { bubbles: true })); } const btn = Array.from(document.querySelectorAll(\"button\")).find(b => b.innerText.includes('Post') || b.type === 'submit'); if(btn) btn.click(); }, content)'.", "3. FALLBACK CLICK: If JS fails, use 'page.locator(\"button[type='submit']\").first.click({force: true})' followed immediately by 'page.keyboard.press(\"Control+Enter\")'.", "4. VERIFICATION LOCK: Do NOT log success unless the window actually closes. If 'page.url()' still contains 'sharer.php' after 15s, throw a 'Strict Failure' error and take a screenshot at 'E:\\hackathon_0_digital_fte\\AI_Employee_vault\\Logs\\FINAL_STRIKE_DEBUG.png'.", "5. CLEANUP: Once published, move the file from /Approved to /Done automatically." ] }

## Response snapshot

Implemented all TITAN-FINAL fixes:

**Fixes Applied**:
1. ✓ ABSOLUTE VIEWPORT: 1920x1200
   - viewport={'width': 1920, 'height': 1200}
   - Post button always in DOM's reachable area

2. ✓ JAVASCRIPT-ONLY SUBMISSION: Direct DOM injection
   - page.evaluate("""(text) => {
       const box = document.querySelector("div[role='textbox']") || 
                   document.querySelector("textarea#xm_0_1") || 
                   document.querySelector("[contenteditable='true']") ||
                   document.querySelector("textarea");
       if (box) {
           if (box.tagName === 'TEXTAREA') box.value = text;
           else box.innerText = text;
           box.dispatchEvent(new Event('input', { bubbles: true }));
           box.dispatchEvent(new Event('change', { bubbles: true }));
           
           const btn = Array.from(document.querySelectorAll("button")).find(b => 
               b.innerText.includes('Post') || b.type === 'submit'
           );
           if (btn) btn.click();
           return 'injected_and_clicked';
       }
       return 'not_found';
     }""", content)
   - Injects content directly into DOM
   - Triggers Post via JS event

3. ✓ FALLBACK CLICK: Force click + Control+Enter
   - submit_btn.click(force=True, timeout=120000)
   - page.keyboard.press('Control+Enter')
   - Immediate fallback if JS fails

4. ✓ VERIFICATION LOCK: 15s strict timeout
   - for i in range(30):  # 30 x 500ms = 15 seconds
   - Check URL change or button disappearance
   - If 'sharer.php' still in URL after 15s:
     - Take screenshot at Logs/FINAL_STRIKE_DEBUG.png
     - Raise Exception("Strict Failure: Window still open after 15s")

5. ✓ CLEANUP: Auto file move
   - post_file_path = metadata.get('_post_file_path')
   - approved_path.rename(done_path)
   - File moved from /Approved/Social to /Done/Social

**Exit Criteria**:
✅ Facebook content is injected directly into the DOM via JavaScript - IMPLEMENTED (JS-only submission)
✅ The 'Post' action is triggered by a direct JS event, bypassing UI visibility issues - IMPLEMENTED (btn.click() via JS)
✅ The file moves to /Done, confirming the entire loop is finished - IMPLEMENTED (auto file move)

**Files Updated**:
- src/skills/meta_poster.py (1920x1200 viewport + JS-only + 15s verification + auto file move)
- src/skills/social_orchestrator.py (pass post_file_path to meta_poster)

## Outcome

- ✅ Impact: Facebook posting now uses pure JS injection with strict 15s verification
- 🧪 Tests: N/A (implementation - user must test Facebook)
- 📁 Files: 2 files updated with TITAN-FINAL implementation
- 🔁 Next prompts: Run social_orchestrator.py --once to test TITAN-FINAL
- 🧠 Reflection: JS-only submission + 15s strict verification + auto file move = complete automation

## Evaluation notes (flywheel)

- Failure modes observed: None (TITAN-FINAL implementation complete)
- Graders run and results: N/A (pending user to test)
- Prompt variant: Phase 3 Facebook TITAN-FINAL
- Next experiment: Run orchestrator, verify JS injection works, window closes in 15s, file moves to /Done
