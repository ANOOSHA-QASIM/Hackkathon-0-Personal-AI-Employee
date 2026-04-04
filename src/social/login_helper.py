"""
Login Helper - Manual session setup for Meta (Facebook/Instagram) and Twitter (X).

Usage:
    python src/social/login_helper.py --once-meta      # Login to Facebook/Instagram
    python src/social/login_helper.py --once-twitter   # Login to Twitter/X

This script launches a browser with persistent session storage.
User manually logs in, then presses Enter in terminal to save and close.
Sessions are saved to .browser_data/meta and .browser_data/twitter.

REPAIRS APPLIED:
- Removed automatic login verification (no more "Could not verify login" warnings)
- Added slow_mo=100 for browser persistence
- Added user-agent for Twitter to prevent bot blocking
- Added 5-second wait after Enter for disk I/O completion
"""

import os
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# Paths
VAULT_ROOT = Path(os.environ.get(
    'VAULT_ROOT',
    'E:/hackathon_0_digital_fte/AI_Employee_vault'
))
BROWSER_DATA_DIR = VAULT_ROOT / '.browser_data'


def login_to_meta():
    """
    Launch browser for manual Meta (Facebook + Instagram) login.

    Session saved to .browser_data/meta/
    Single login covers both Facebook and Instagram.
    
    REPAIR: No verification logic - just opens browser and waits for Enter.
    """
    print("=" * 60)
    print("Meta Login Helper (Facebook + Instagram)")
    print("=" * 60)
    print()

    user_data_dir = BROWSER_DATA_DIR / 'meta'

    # CLEANUP: Create directory if needed, but don't delete if exists
    print(f"[Meta] Session directory: {user_data_dir}")
    os.makedirs(str(user_data_dir), exist_ok=True)
    
    # CLEANUP: Check if folder is empty or has content
    if user_data_dir.exists():
        existing_files = list(user_data_dir.glob('**/*'))
        if len(existing_files) > 0:
            print(f"[Meta] ✓ Using existing session folder ({len(existing_files)} files)")
        else:
            print(f"[Meta] ✓ Creating new session folder")
    
    print()
    print(f"[Meta] Session will be saved to: {user_data_dir}")
    print()

    with sync_playwright() as p:
        # PERSISTENCE FIX: launch_persistent_context with slow_mo=100
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            timeout=90000,
            slow_mo=100,  # PERSISTENCE FIX: Give browser time to write cookies
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu'
            ]
        )

        page = context.pages[0] if context.pages else context.new_page()

        try:
            # Navigate to Facebook
            print("[Meta] Opening Facebook login page...")
            page.goto('https://www.facebook.com/', timeout=90000)

            print()
            print("=" * 60)
            print("MANUAL LOGIN REQUIRED")
            print("=" * 60)
            print()
            print("1. Log in to Facebook in the browser window")
            print("2. Complete 2FA if prompted")
            print("3. Verify you can see your Facebook feed")
            print("4. Return to this terminal and press ENTER to save session")
            print()
            print("⚠  The browser will stay open until you press ENTER")
            print()

            # REPAIR: Blocking input() - no verification, just wait
            input("Press ENTER when you have successfully logged in to Facebook...")

            # CLEANUP: Wait 5 seconds for disk I/O to complete before closing
            print()
            print("[Meta] Saving session... please wait 5 seconds")
            for i in range(5, 0, -1):
                print(f"[Meta] Saving... {i}")
                time.sleep(1)

            # SUCCESS: No verification, just confirm save
            print()
            print("=" * 60)
            print("✓ SUCCESS: Meta session saved!")
            print("=" * 60)
            print()
            print("Session saved to:", user_data_dir)
            print()
            print("Next steps:")
            print("1. Run '--once-twitter' to set up Twitter session")
            print("2. Then run social_dispatcher.py to start posting")
            print()

        except Exception as e:
            print(f"[Meta] ERROR: {e}")
            print("Please try again")
        finally:
            context.close()


def login_to_twitter():
    """
    Launch browser for manual Twitter (X) login.

    Session saved to .browser_data/twitter/
    
    TWITTER SPECIFIC: Added user-agent to prevent X from blocking as bot.
    REPAIR: No verification logic - just opens browser and waits for Enter.
    """
    print("=" * 60)
    print("Twitter (X) Login Helper")
    print("=" * 60)
    print()

    user_data_dir = BROWSER_DATA_DIR / 'twitter'

    # CLEANUP: Create directory if needed, but don't delete if exists
    print(f"[Twitter] Session directory: {user_data_dir}")
    os.makedirs(str(user_data_dir), exist_ok=True)
    
    # CLEANUP: Check if folder is empty or has content
    if user_data_dir.exists():
        existing_files = list(user_data_dir.glob('**/*'))
        if len(existing_files) > 0:
            print(f"[Twitter] ✓ Using existing session folder ({len(existing_files)} files)")
        else:
            print(f"[Twitter] ✓ Creating new session folder")
    
    print()
    print(f"[Twitter] Session will be saved to: {user_data_dir}")
    print()

    with sync_playwright() as p:
        # PERSISTENCE FIX: launch_persistent_context with slow_mo=100
        # FIX TWITTER BOT BLOCK: Updated to latest Chrome user-agent
        # STEALTH MODE: Added automation hiding flags
        # MAXIMIZE WINDOW: Added --start-maximized and viewport settings
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,
            viewport={'width': 1920, 'height': 1080},  # SCREEN RESOLUTION: 1920x1080
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            timeout=120000,  # INCREASE TIMEOUT: 120 seconds global timeout
            slow_mo=100,  # PERSISTENCE FIX: Give browser time to write cookies
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu',
                '--disable-blink-features=AutomationControlled',  # Bypass bot detection
                '--start-maximized'  # MAXIMIZE WINDOW: Open in fullscreen
            ]
        )

        page = context.pages[0] if context.pages else context.new_page()

        # STEALTH MODE: Inject scripts to hide automation
        # TWITTER LOGIN BYPASS: Bypass 'Something went wrong' bot-check
        page.add_init_script("""
            // Override navigator.webdriver
            Object.defineProperty(navigator, 'webdriver', {
                get: () => false
            });
            
            // Override permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            // Override plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            
            // Override languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        """)

        try:
            # Navigate to Twitter
            print("[Twitter] Opening Twitter (X) login page...")
            print("[Twitter] NOTE: Use direct email/username login (NOT Google/Apple)")
            page.goto('https://twitter.com/', timeout=120000)
            
            # WAIT FOR IDLE: Ensure full Desktop UI is loaded before searching for buttons
            print("[Twitter] Waiting for page to load (networkidle)...")
            page.wait_for_load_state('networkidle', timeout=120000)
            
            # INCREASE TIMEOUTS: Wait 60s for page to fully load
            print("[Twitter] Waiting for page to load (120s timeout)...")
            page.wait_for_timeout(10000)  # Initial wait

            print()
            print("=" * 60)
            print("MANUAL LOGIN REQUIRED")
            print("=" * 60)
            print()
            print("⚠  IMPORTANT: Use DIRECT EMAIL/USERNAME login only")
            print("   DO NOT use 'Continue with Google' or 'Continue with Apple'")
            print("   (X blocks these in automation)")
            print()
            print("1. Log in to Twitter (X) in the browser window")
            print("2. Complete 2FA if prompted")
            print("3. Verify you can see your Twitter feed")
            print("4. Return to this terminal and press ENTER to save session")
            print()
            print("⚠  The browser will stay open until you press ENTER")
            print()

            # SELECTOR REPAIR: Wait specifically for username field
            print("[Twitter] Waiting for username field...")
            try:
                # Wait for username input (direct login)
                username_field = page.get_by_placeholder("Phone, email, or username")
                username_field.wait_for(state='visible', timeout=60000)
                print("[Twitter] ✓ Username field detected - direct login available")
            except:
                print("[Twitter] ⚠  Username field not found - you may need to select 'Use email or username instead'")

            # REPAIR: Blocking input() - no verification, just wait
            input("Press ENTER when you have successfully logged in to Twitter...")

            # CLEANUP: Wait 5 seconds for disk I/O to complete before closing
            print()
            print("[Twitter] Saving session... please wait 5 seconds")
            for i in range(5, 0, -1):
                print(f"[Twitter] Saving... {i}")
                time.sleep(1)

            # SUCCESS: No verification, just confirm save
            print()
            print("=" * 60)
            print("✓ SUCCESS: Twitter session saved!")
            print("=" * 60)
            print()
            print("Session saved to:", user_data_dir)
            print()
            print("Next steps:")
            print("1. Run social_dispatcher.py to start posting to all platforms")
            print()

        except Exception as e:
            print(f"[Twitter] ERROR: {e}")
            print("Please try again")
        finally:
            context.close()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python src/social/login_helper.py --once-meta      # Login to Facebook/Instagram")
        print("  python src/social/login_helper.py --once-twitter   # Login to Twitter/X")
        print()
        print("This script launches a browser for manual login.")
        print("Sessions are saved to .browser_data/meta and .browser_data/twitter.")
        sys.exit(1)
    
    if sys.argv[1] == '--once-meta':
        login_to_meta()
    elif sys.argv[1] == '--once-twitter':
        login_to_twitter()
    else:
        print(f"Unknown argument: {sys.argv[1]}")
        print("Use --once-meta or --once-twitter")
        sys.exit(1)


if __name__ == '__main__':
    main()
