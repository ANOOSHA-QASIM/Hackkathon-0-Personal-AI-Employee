"""
LinkedIn Login Assistant - Opens browser for manual LinkedIn login.

Usage:
    python src/linkedin/login_assistant.py

This script ONLY launches a persistent Chromium browser to LinkedIn login page.
It waits 120 seconds for you to log in manually, then closes.
The session is saved to .browser_data/linkedin for future use.
"""

import time
from pathlib import Path
from playwright.sync_api import sync_playwright

# Paths
VAULT_ROOT = Path(__file__).parent.parent.parent
BROWSER_DATA_DIR = VAULT_ROOT / '.browser_data' / 'linkedin'


def main():
    """Launch browser for manual LinkedIn login."""
    print("=" * 60)
    print("LinkedIn Login Assistant")
    print("=" * 60)
    print()
    print("This will open a browser window to LinkedIn login.")
    print("You have 120 seconds to log in manually.")
    print("Your session will be saved for future automatic posting.")
    print()
    print("Opening browser...")
    
    # Ensure data directory exists
    BROWSER_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    with sync_playwright() as p:
        # Launch persistent browser (visible mode)
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(BROWSER_DATA_DIR),
            headless=False,  # Visible browser
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        
        try:
            # Navigate to LinkedIn login
            print("Navigating to https://www.linkedin.com/login...")
            page.goto('https://www.linkedin.com/login', timeout=60000)
            
            print()
            print("=" * 60)
            print("Browser is now open.")
            print("Please log in to LinkedIn in the browser window.")
            print("The browser will stay open for 120 seconds.")
            print("After successful login, the session will be saved.")
            print("=" * 60)
            print()
            
            # Wait 120 seconds for user to log in
            for i in range(24):  # 120 seconds / 5 second intervals
                time.sleep(5)
                
                # Check if user is logged in (look for profile icon or feed)
                is_logged_in = (
                    page.query_selector('.profile-nav__profile-photo') or
                    page.query_selector('.share-box-feed-entry__trigger') or
                    page.query_selector('a[href*="/mynetwork/"]')
                )
                
                if is_logged_in:
                    print()
                    print("✓ Login detected! Session will be saved.")
                    print("You can close the browser or wait for timeout.")
                    # Continue waiting so user can verify
                    break
            
            # Final countdown
            print()
            print("Browser will close in 10 seconds...")
            time.sleep(10)
            
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")
        finally:
            context.close()
    
    print()
    print("=" * 60)
    print("Session saved to:", BROWSER_DATA_DIR)
    print()
    print("Next steps:")
    print("1. Run: python src/linkedin/linkedin_poster.py --once")
    print("2. The poster will now use your saved session")
    print("3. No need to log in again (unless session expires)")
    print("=" * 60)


if __name__ == '__main__':
    main()
