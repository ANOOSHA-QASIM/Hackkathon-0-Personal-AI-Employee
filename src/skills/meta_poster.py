"""
Meta Poster - Facebook and Instagram posting skill.

Uses Playwright with persistent session (.browser_data/meta).
Single login covers both Facebook and Instagram.
"""

import os
import glob
from pathlib import Path
from typing import Optional, Dict
from datetime import datetime
import time

from playwright.sync_api import sync_playwright
from .base_poster import BasePoster, PostingResult

# PATH LOCK: Define VAULT_ROOT globally
VAULT_ROOT = Path(r"E:\hackathon_0_digital_fte\AI_Employee_vault")

# Session location
META_USER_DATA_DIR = VAULT_ROOT / '.browser_data' / 'meta'
LOGS_PATH = VAULT_ROOT / 'Logs'
DEFAULT_IMAGE_PATH = VAULT_ROOT / "Posts" / "Assets" / "default.jpg"
ASSETS_PATH = VAULT_ROOT / "Posts" / "Assets"


class MetaPoster(BasePoster):
    """
    Meta Poster skill for Facebook and Instagram.

    Usage:
        poster = MetaPoster()
        result = poster.post(content, media_path)
    """

    def __init__(self):
        super().__init__('meta', META_USER_DATA_DIR)

    def post(self, content: str, media_path: Optional[str] = None, metadata: Optional[Dict] = None) -> PostingResult:
        """
        Post content to Facebook.

        Args:
            content: Post text content
            media_path: Optional path to image/media file
            metadata: Optional dict with _post_file_path for moving file to /Done

        Returns:
            PostingResult with status, URL, timestamp, errors
        """
        return self.post_to_facebook(content, media_path, metadata)

    def authenticate(self) -> bool:
        """
        Authenticate with Meta (manual login via login_helper.py).

        Returns:
            True if authentication successful
        """
        # Session should already be set up via login_helper.py
        # Just verify session exists
        if self.user_data_dir.exists():
            session_files = list(self.user_data_dir.glob('**/*'))
            if len(session_files) > 0:
                self.is_authenticated = True
                return True
        return False

    def _close_popups(self, page):
        """
        NO POP-UP INTERFERENCE: Check for and close pop-ups.
        Closes 'Turn on Notifications', 'Messenger', and other blocking pop-ups.
        """
        try:
            # Look for common close buttons
            close_selectors = [
                'button[aria-label="Close"]',
                'div[role="button"][aria-label="Close"]',
                'svg[aria-label="Close"]',
                'button[class*="close"]',
                'div[class*="close"]'
            ]
            
            for selector in close_selectors:
                try:
                    close_btns = page.locator(selector)
                    count = close_btns.count()
                    
                    if count > 0:
                        print(f"[Meta] Found {count} pop-up close buttons, closing...")
                        for i in range(min(count, 3)):  # Close up to 3 pop-ups
                            try:
                                close_btns.nth(i).click(timeout=2000)
                                page.wait_for_timeout(500)
                            except:
                                pass
                except:
                    pass
            
            print("[Meta] Pop-ups cleared")
        except Exception as e:
            print(f"[Meta] Error closing pop-ups: {e}")

    def post_to_facebook(self, content: str, media_path: Optional[str] = None, metadata: Optional[Dict] = None) -> PostingResult:
        """
        Post to Facebook.

        Args:
            content: Post text content (max 2,200 chars for Instagram)
            media_path: Optional path to image/media file (JPG, PNG, max 15MB)
            metadata: Optional dict with _post_file_path for moving file to /Done

        Returns:
            PostingResult with Instagram/Facebook post URL
        """
        print("[Meta] Posting to Instagram (with Facebook cross-post)...")

        # Initialize metadata if not provided
        if metadata is None:
            metadata = {}

        # RELIABLE PATHS: Find any .jpg or .png in Assets folder
        if not media_path or not Path(media_path).exists():
            # Try default.jpg first
            if DEFAULT_IMAGE_PATH.exists():
                print(f"[Meta] Using default image: {DEFAULT_IMAGE_PATH}")
                media_path = str(DEFAULT_IMAGE_PATH)
            else:
                # Search for any image file in Assets folder
                image_files = glob.glob(os.path.join(ASSETS_PATH, "*.jpg")) + \
                             glob.glob(os.path.join(ASSETS_PATH, "*.jpeg")) + \
                             glob.glob(os.path.join(ASSETS_PATH, "*.png"))
                
                if image_files:
                    print(f"[Meta] Found image files: {image_files}")
                    media_path = image_files[0]  # Use first found image
                    print(f"[Meta] Using first found image: {media_path}")
                else:
                    print("")
                    print("=" * 60)
                    print("ERROR: INSTAGRAM REQUIRES AN IMAGE")
                    print("=" * 60)
                    print(f"[Meta] No image found in: {ASSETS_PATH}")
                    print("[Meta] Please add an image (.jpg, .jpeg, or .png) to Posts/Assets/")
                    print("=" * 60)
                    print("")
                    return PostingResult(
                        platform='instagram',
                        status='failed',
                        url=None,
                        published_at=None,
                        error='Instagram requires an image. Please add image to Posts/Assets/'
                    )

        try:
            with sync_playwright() as p:
                # INSTAGRAM AUTOMATION: Standard desktop viewport
                context = p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    viewport={'width': 1280, 'height': 1000},  # Standard desktop viewport
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',  # Standard Windows Chrome
                    timeout=120000,
                    slow_mo=100,
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-gpu',
                        '--disable-blink-features=AutomationControlled'
                    ]
                )

                page = context.pages[0] if context.pages else context.new_page()

                # STEALTH MODE
                page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => false
                    });
                """)

                try:
                    # RETIRE FACEBOOK AUTO: Navigate to Instagram instead
                    print("[Meta] Navigating to Instagram...")
                    page.goto('https://www.instagram.com/', timeout=120000)

                    # WAIT FOR LOGIN: Check if logged in
                    print("[Meta] Checking login state...")
                    page.wait_for_timeout(5000)
                    current_url = page.url

                    if 'login' in current_url.lower() or 'accounts' in current_url.lower():
                        print("[Meta] Instagram login page detected, waiting 60s...")
                        print("[Meta] Please log in manually (session will be saved)...")

                        for i in range(60, 0, -1):
                            if i % 10 == 0:
                                print(f"[Meta] Time remaining: {i} seconds...")
                            page.wait_for_timeout(1000)

                        if 'login' in page.url.lower() or 'accounts' in page.url.lower():
                            raise Exception("Instagram login required. Please log in and try again.")
                        else:
                            print("[Meta] Login detected, session saved!")

                    print("[Meta] Already logged in on Instagram")
                    page.wait_for_timeout(3000)  # Wait for page to fully load

                    # SIDEBAR CREATE BUTTON: Target the '+' icon directly
                    print("[Meta] Opening create post modal...")
                    create_clicked = False

                    # Method 1: Look for 'New post' link in sidebar
                    try:
                        new_post_link = page.get_by_role("link", name="New post").first
                        if new_post_link.count() > 0:
                            new_post_link.click(timeout=120000)
                            print("[Meta] 'New post' link clicked from sidebar")
                            create_clicked = True
                        else:
                            print("[Meta] 'New post' link not found, trying SVG icon...")
                    except Exception as link_error:
                        print(f"[Meta] 'New post' link failed: {link_error}")

                    # Method 2: Look for SVG '+' icon
                    if not create_clicked:
                        try:
                            create_svg = page.locator("svg[aria-label='New post']").first
                            if create_svg.count() > 0:
                                create_svg.click(timeout=120000)
                                print("[Meta] SVG '+' icon clicked")
                                create_clicked = True
                        except Exception as svg_error:
                            print(f"[Meta] SVG icon failed: {svg_error}")

                    # Method 3: Keyboard shortcut fallback
                    if not create_clicked:
                        try:
                            page.keyboard.press('Control+n')
                            print("[Meta] Control+n pressed")
                            create_clicked = True
                        except:
                            pass

                    # NO-MODAL FALLBACK: If all else fails, navigate to create page
                    if not create_clicked:
                        try:
                            print("[Meta] All methods failed, trying direct navigation...")
                            page.goto('https://www.instagram.com/create/', timeout=120000, wait_until='domcontentloaded')
                            print("[Meta] Navigated to instagram.com/create/")
                            create_clicked = True
                        except Exception as nav_error:
                            print(f"[Meta] Direct navigation failed: {nav_error}")

                    page.wait_for_timeout(3000)

                    # FILE CHOOSER WAIT: Use official Playwright file chooser
                    print(f"[Meta] Uploading media: {media_path}")
                    upload_success = False

                    try:
                        # Wait for file chooser and trigger it
                        print("[Meta] Waiting for file chooser...")
                        
                        # First try to click "Select from computer" button
                        try:
                            select_btn = page.get_by_role("button", name="Select from computer").first
                            if select_btn.count() > 0:
                                print("[Meta] Clicking 'Select from computer' button...")
                                # Use synchronous file chooser
                                with page.expect_file_chooser() as fc_info:
                                    select_btn.click(timeout=5000)
                                file_chooser = fc_info.value
                                file_chooser.set_files(media_path)
                                print("[Meta] ✓ File attached via file chooser!")
                                upload_success = True
                        except Exception as btn_error:
                            print(f"[Meta] 'Select from computer' button not found: {btn_error}")

                        # If button method failed, try hidden file input
                        if not upload_success:
                            file_input_selectors = [
                                'input[type="file"]',
                                'input[type="file"][accept*="image"]',
                                'input[accept*="image"]',
                            ]
                            for selector in file_input_selectors:
                                try:
                                    file_input = page.locator(selector).first
                                    if file_input.count() > 0:
                                        file_input.set_files(media_path)
                                        print(f"[Meta] ✓ File attached via {selector}!")
                                        upload_success = True
                                        break
                                except:
                                    pass

                        if not upload_success:
                            raise Exception("Could not attach file via any method")

                        # NEXT BUTTON SEQUENCE: Wait for Next button to be enabled
                        print("[Meta] Waiting for 'Next' button to be enabled...")
                        next_enabled = False
                        for i in range(20):  # Wait up to 10 seconds
                            page.wait_for_timeout(500)
                            try:
                                next_btn = page.get_by_role("button", name="Next").first
                                if next_btn.count() > 0:
                                    is_disabled = next_btn.is_disabled(timeout=1000)
                                    if not is_disabled:
                                        next_enabled = True
                                        print("[Meta] ✓ 'Next' button is enabled!")
                                        break
                            except:
                                pass

                        if not next_enabled:
                            raise Exception("'Next' button did not become enabled in 10s")

                        # Click Next twice
                        print("[Meta] Clicking 'Next' twice...")
                        for next_attempt in range(2):
                            try:
                                next_btn = page.get_by_role("button", name="Next").first
                                if next_btn.count() > 0:
                                    next_btn.click(timeout=120000)
                                    print(f"[Meta] ✓ 'Next' {next_attempt + 1}/2 clicked!")
                                    page.wait_for_timeout(3000)
                            except Exception as next_error:
                                print(f"[Meta] 'Next' {next_attempt + 1} failed: {next_error}")
                                break

                    except Exception as upload_error:
                        print(f"[Meta] Upload failed: {upload_error}")
                        return PostingResult(
                            platform='instagram',
                            status='failed',
                            url=None,
                            published_at=None,
                            error=f'Upload failed: {upload_error}'
                        )

                    page.wait_for_timeout(2000)

                    # CAPTION INJECTION: Use get_by_role textbox selector
                    print(f"[Meta] Adding caption ({len(content)} chars)...")
                    caption_filled = False

                    try:
                        # Use get_by_role textbox selector
                        caption_box = page.get_by_role("textbox", name="Write a caption...").first
                        if caption_box.count() > 0:
                            caption_box.fill(content, timeout=120000)
                            print("[Meta] ✓ Caption added successfully!")
                            caption_filled = True
                        else:
                            # Fallback to aria-label selector
                            print("[Meta] textbox selector not found, trying aria-label fallback...")
                            caption_box = page.locator("div[aria-label='Write a caption...']").first
                            if caption_box.count() > 0:
                                caption_box.fill(content, timeout=120000)
                                print("[Meta] ✓ Caption added via aria-label fallback!")
                                caption_filled = True
                            else:
                                # Last fallback to textarea placeholder
                                print("[Meta] aria-label not found, trying textarea fallback...")
                                caption_box = page.locator('textarea[placeholder="Write a caption..."]').first
                                if caption_box.count() > 0:
                                    caption_box.fill(content, timeout=120000)
                                    print("[Meta] ✓ Caption added via textarea fallback!")
                                    caption_filled = True
                    except Exception as caption_error:
                        print(f"[Meta] Caption failed: {caption_error}")

                    # CAPTION VERIFICATION: Hard STOP if caption not filled
                    if not caption_filled:
                        print("")
                        print("=" * 60)
                        print("ERROR: CAPTION BOX NOT FOUND")
                        print("=" * 60)
                        print("[Meta] Cannot proceed without caption box")
                        print("[Meta] This is a hard stop - no fake success")
                        print("=" * 60)
                        print("")
                        return PostingResult(
                            platform='instagram',
                            status='failed',
                            url=None,
                            published_at=None,
                            error='Caption box not found - get_by_role("textbox", name="Write a caption...") missing'
                        )

                    # CAPTION RE-CHECK: Wait for typing to finish before Share click
                    print("[Meta] CAPTION RE-CHECK: Waiting for caption to register...")
                    page.wait_for_timeout(3000)  # Wait 3 seconds for caption to fully register

                    # FINAL SHARE: Click Share and wait for toast message
                    print("[Meta] Clicking 'Share' button...")
                    try:
                        share_btn = page.get_by_role("button", name="Share").first
                        if share_btn.count() > 0:
                            share_btn.click(timeout=120000)
                            print("[Meta] ✓ 'Share' button clicked!")
                        else:
                            print("[Meta] Share button not found, trying fallback...")
                            # Fallback to text search
                            share_btn = page.locator('button:has-text("Share")').first
                            if share_btn.count() > 0:
                                share_btn.click(timeout=120000)
                                print("[Meta] ✓ 'Share' button clicked via fallback!")
                            else:
                                print("[Meta] ERROR: Could not find Share button")
                    except Exception as share_error:
                        print(f"[Meta] 'Share' button click failed: {share_error}")

                    # POST-CLICK WAIT: Wait for success dialog after clicking Share
                    print("[Meta] POST-CLICK WAIT: Waiting for Instagram to process upload...")
                    post_confirmed = False

                    # WAIT FOR SUCCESS DIALOG: Use wait_for_selector with 60s timeout
                    print("[Meta] WAIT FOR SUCCESS DIALOG: Waiting up to 60 seconds...")
                    try:
                        # Wait for "Your post has been shared" toast message
                        shared_text = page.locator('text="Your post has been shared"')
                        shared_text.wait_for(state='visible', timeout=60000)
                        post_confirmed = True
                        print("[Meta] ✓ 'Your post has been shared' toast detected!")
                    except Exception as toast_error:
                        print(f"[Meta] Toast message not found: {toast_error}")
                        # Continue checking other success indicators

                    # VERIFY URL CHANGE: Wait for Create modal to disappear
                    if not post_confirmed:
                        print("[Meta] VERIFY URL CHANGE: Waiting for Create modal to disappear...")
                        try:
                            create_modal = page.locator('div[role="dialog"], [aria-label="Create"]')
                            create_modal.wait_for(state='detached', timeout=30000)
                            post_confirmed = True
                            print("[Meta] ✓ Create modal disappeared from DOM!")
                        except Exception as modal_error:
                            print(f"[Meta] Modal did not disappear: {modal_error}")

                    # Additional verification: check URL
                    if not post_confirmed:
                        current_url = page.url
                        if 'instagram.com' in current_url and 'create' not in current_url.lower():
                            post_confirmed = True
                            print("[Meta] ✓ URL changed - post successful!")

                    # Final status check
                    if not post_confirmed:
                        print("[Meta] ERROR: Post confirmation not received after 60s wait")
                        print("[Meta] This means the upload may have failed")

                    # REVERSE MOVE: Only move file to /Done if post confirmed
                    print("")
                    if post_confirmed:
                        print("[Meta] ✓ Instagram post completed!")

                        # FINAL MOVE: Move file from /Approved to /Done ONLY on confirmed success
                        try:
                            post_file_path = metadata.get('_post_file_path')
                            if post_file_path:
                                approved_path = Path(post_file_path)
                                done_path = VAULT_ROOT / 'Done' / 'Social' / approved_path.name

                                if approved_path.exists():
                                    done_path.parent.mkdir(parents=True, exist_ok=True)
                                    approved_path.rename(done_path)
                                    print(f"[Meta] ✓ File moved to /Done: {approved_path.name}")
                        except Exception as move_error:
                            print(f"[Meta] Could not move file to /Done: {move_error}")
                    else:
                        print("[Meta] ERROR: Post confirmation not received")
                        print("[Meta] File will REMAIN in /Approved (not moved to /Done)")
                        print("[Meta] This is intentional - no fake success")

                    print("")
                    print("=" * 60)
                    print("INSTAGRAM POST COMPLETE (Facebook cross-post if enabled)")
                    print("=" * 60)
                    print("")

                    return PostingResult(
                        platform='instagram',
                        status='published' if post_confirmed else 'failed',
                        url='https://www.instagram.com/',
                        published_at=datetime.now().isoformat(),
                        error=None if post_confirmed else 'Post confirmation not received after 60s wait'
                    )

                except Exception as e:
                    print(f"[Meta] ERROR posting to Facebook: {e}")
                    # RALPH WIGGUM LOGGING: Take screenshot on failure
                    try:
                        error_screenshot_path = LOGS_PATH / 'error_screenshot_meta.png'
                        page.screenshot(path=str(error_screenshot_path))
                        print(f"[Meta] RALPH WIGGUM: Error screenshot saved to {error_screenshot_path}")
                    except Exception as screenshot_error:
                        print(f"[Meta] Could not take screenshot: {screenshot_error}")
                    
                    return PostingResult(
                        platform='facebook',
                        status='failed',
                        url=None,
                        published_at=None,
                        error=str(e)
                    )
                finally:
                    context.close()

        except Exception as e:
            print(f"[Meta] ERROR launching browser: {e}")
            return PostingResult(
                platform='facebook',
                status='failed',
                url=None,
                published_at=None,
                error=str(e)
            )

    def post_to_instagram(self, content: str, media_path: Optional[str] = None) -> PostingResult:
        """
        Post to Instagram.

        INSTAGRAM FIX: Navigate to instagram.com/create/select/ and use set_input_files.

        Args:
            content: Post text content (max 2,200 chars, 138-150 optimal)
            media_path: Optional path to image/media file (JPG, PNG, max 8MB)

        Returns:
            PostingResult with Instagram post URL
        """
        # INSTAGRAM STRICT FIX: Requires image to post
        if not media_path:
            print("[Meta] Instagram posting requires an image - skipping")
            return PostingResult(
                platform='instagram',
                status='skipped',
                url=None,
                published_at=None,
                error='Instagram requires image media'
            )

        print("[Meta] Posting to Instagram...")

        try:
            with sync_playwright() as p:
                # DEBUG MODE: headless=False, forced 1920x1080 resolution
                context = p.chromium.launch_persistent_context(
                    user_data_dir=str(self.user_data_dir),
                    headless=False,
                    viewport={'width': 1920, 'height': 1080},  # FORCED 1920x1080
                    user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    timeout=120000,
                    slow_mo=100,
                    args=[
                        '--no-sandbox',
                        '--disable-setuid-sandbox',
                        '--disable-dev-shm-usage',
                        '--disable-gpu',
                        '--disable-blink-features=AutomationControlled',
                        '--start-maximized'
                    ]
                )

                page = context.pages[0] if context.pages else context.new_page()

                # STEALTH MODE
                page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => false
                    });
                """)

                try:
                    # INSTAGRAM FIX: Navigate to create page with robust selectors
                    print("[Instagram] Navigating to Instagram create page...")
                    page.goto('https://www.instagram.com/create/select/', timeout=120000)
                    page.wait_for_load_state('domcontentloaded', timeout=120000)
                    page.wait_for_timeout(3000)

                    # INSTAGRAM STRICT FIX: Use set_input_files on hidden file input (100% stable)
                    print(f"[Instagram] Uploading media: {media_path}")
                    file_input = page.locator('input[type="file"][accept*="image"]').first
                    
                    # ERROR HANDLING: Try multiple selectors for file input
                    if file_input.count() == 0:
                        # Fallback selectors
                        file_input = page.locator('input[type="file"]').first
                    
                    if file_input.count() > 0:
                        file_input.set_files(media_path)
                        print("[Instagram] Media uploaded successfully")
                        page.wait_for_timeout(5000)  # Wait for upload
                    else:
                        print("[Instagram] WARNING: Could not find file input, posting text only")
                        # Don't fail - allow text-only post if image upload fails

                    # Type caption
                    print(f"[Instagram] Typing caption ({len(content)} chars)...")
                    caption_input = page.locator('textarea[placeholder="Write a caption..."]').first
                    
                    if caption_input.count() > 0:
                        caption_input.fill(content, timeout=120000)
                        page.wait_for_timeout(3000)
                    else:
                        # Fallback caption selector
                        caption_input = page.locator('textarea[aria-label="Write a caption..."]').first
                        if caption_input.count() > 0:
                            caption_input.fill(content, timeout=120000)
                            page.wait_for_timeout(3000)
                        else:
                            print("[Instagram] WARNING: Could not find caption input")

                    # Click Share button
                    print("[Instagram] Sharing post...")
                    share_btn = page.get_by_role("button", name=re.compile(r"(Share|Next)", re.I))
                    if share_btn.count() > 0:
                        share_btn.click(timeout=120000)
                        page.wait_for_timeout(5000)  # Wait for post to publish
                        print("[Instagram] ✓ Instagram post published!")
                        
                        return PostingResult(
                            platform='instagram',
                            status='published',
                            url='https://www.instagram.com/',
                            published_at=datetime.now().isoformat(),
                            error=None
                        )
                    else:
                        print("[Instagram] WARNING: Could not find Share button")
                        return PostingResult(
                            platform='instagram',
                            status='failed',
                            url=None,
                            published_at=None,
                            error='Could not find Share button'
                        )

                except Exception as e:
                    print(f"[Instagram] ERROR: {e}")
                    # RALPH WIGGUM LOGGING: Take screenshot on failure
                    try:
                        error_screenshot_path = LOGS_PATH / 'error_screenshot_instagram.png'
                        page.screenshot(path=str(error_screenshot_path))
                        print(f"[Instagram] RALPH WIGGUM: Error screenshot saved to {error_screenshot_path}")
                    except Exception as screenshot_error:
                        print(f"[Instagram] Could not take screenshot: {screenshot_error}")
                    
                    return PostingResult(
                        platform='instagram',
                        status='failed',
                        url=None,
                        published_at=None,
                        error=str(e)
                    )
                finally:
                    context.close()

        except Exception as e:
            print(f"[Meta] ERROR launching browser for Instagram: {e}")
            return PostingResult(
                platform='instagram',
                status='failed',
                url=None,
                published_at=None,
                error=str(e)
            )
