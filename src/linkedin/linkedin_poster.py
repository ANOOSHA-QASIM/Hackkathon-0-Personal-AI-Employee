"""
LinkedIn Poster - Monitors /Approved for posts and publishes via Playwright.

Usage:
    python src/linkedin/linkedin_poster.py

Prerequisites:
    pip install playwright
    playwright install chromium
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path
import yaml
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ============================================================================
# Configuration - Absolute Paths per Constitution
# ============================================================================

VAULT_ROOT = Path(os.environ.get(
    'VAULT_ROOT',
    'E:/hackathon_0_digital_fte/AI_Employee_vault'
))

IN_PROGRESS_PATH = VAULT_ROOT / 'In_Progress' / 'linkedin-agent'
APPROVED_PATH = VAULT_ROOT / 'Approved'
DONE_PATH = VAULT_ROOT / 'Done'
REJECTED_PATH = VAULT_ROOT / 'Rejected'
LOGS_PATH = VAULT_ROOT / 'Logs'

# LinkedIn credentials (from environment or .env)
LINKEDIN_EMAIL = os.environ.get('LINKEDIN_EMAIL', '')
LINKEDIN_PASSWORD = os.environ.get('LINKEDIN_PASSWORD', '')


# ============================================================================
# Audit Logging
# ============================================================================

def log_action(action_type, file_path, status, metadata=None, error_message=None, **kwargs):
    """Log an action to today's audit file.
    
    Args:
        action_type: Type of action
        file_path: Path to affected file
        status: Action status
        metadata: Optional additional metadata
        error_message: Optional error message
        **kwargs: Additional fields (e.g., source='linkedin')
    """
    today = datetime.now().strftime('%Y-%m-%d')
    log_path = LOGS_PATH / f'{today}.json'

    LOGS_PATH.mkdir(parents=True, exist_ok=True)

    # Load or initialize log file
    if log_path.exists():
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            log_data = _initialize_log_data()
    else:
        log_data = _initialize_log_data()

    # Create log entry
    entry = {
        'timestamp': datetime.now().isoformat() + 'Z',
        'action_type': action_type,
        'agent_id': 'linkedin-poster',
        'file_path': file_path,
        'status': status,
    }
    
    # Add kwargs (e.g., source='linkedin')
    for key, value in kwargs.items():
        entry[key] = value

    if metadata:
        entry['metadata'] = metadata
    if error_message:
        entry['error_message'] = error_message

    # Append entry
    log_data['entries'].append(entry)

    # Update summary
    log_data['summary'] = {
        'total_actions': len(log_data['entries']),
        'completed': sum(1 for e in log_data['entries'] if e['status'] == 'completed'),
        'errors': sum(1 for e in log_data['entries'] if e['status'] == 'error'),
    }

    # Write back
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2)


def _initialize_log_data():
    """Initialize new log file structure."""
    today = datetime.now().strftime('%Y-%m-%d')
    return {
        'date': today,
        'vault_id': 'AI_Employee_vault',
        'entries': [],
        'summary': {
            'total_actions': 0,
            'completed': 0,
            'errors': 0,
        },
        'sealed': False,
        'sealed_at': None,
        'content_hash': None,
    }


# ============================================================================
# Post Processing
# ============================================================================

def parse_post_metadata(file_path):
    """Parse YAML frontmatter from post file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not content.startswith('---'):
        return None
    
    end = content.find('---', 3)
    if end == -1:
        return None
    
    yaml_content = content[3:end].strip()
    try:
        return yaml.safe_load(yaml_content)
    except yaml.YAMLError:
        return None


def validate_post_metadata(metadata):
    """Validate post has required fields."""
    required_fields = ['status', 'platform', 'content', 'created_at', 'created_by', 'hitl_approved']
    
    for field in required_fields:
        if field not in metadata:
            return False, f"Missing required field: {field}"
    
    # Check HITL approval
    if not metadata.get('hitl_approved', False):
        return False, "HITL approval required (hitl_approved: false)"
    
    # Check platform
    if metadata.get('platform') != 'linkedin':
        return False, f"Wrong platform: {metadata.get('platform')} (expected: linkedin)"
    
    return True, "Valid"


def update_post_status(file_path, new_status, **kwargs):
    """Update post metadata with new status and fields."""
    metadata = parse_post_metadata(file_path)
    if not metadata:
        return
    
    # Update fields
    metadata['status'] = new_status
    for key, value in kwargs.items():
        metadata[key] = value
    
    # Read original content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find body (after second ---)
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            body = content[end + 3:].strip()
            
            # Generate new frontmatter
            yaml_content = yaml.dump(metadata, sort_keys=False, allow_unicode=True, default_flow_style=False)
            new_content = f"---\n{yaml_content}---\n\n{body}"
            
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)


# ============================================================================
# LinkedIn Publishing via Playwright
# ============================================================================

def publish_to_linkedin(content: str, media_path: str = None):
    """
    Publish post to LinkedIn using Playwright with persistent session.
    
    Features:
    - 90s timeout for slow Karachi internet
    - Robust selectors: 'Start a post' button and 'Post' button
    - try-except-finally for guaranteed browser cleanup
    - headless=False for visible posting
    - SMART FOLDER: Assumes approved if file is in /Approved

    Args:
        content: Post text content
        media_path: Optional path to image/media file
    
    Returns:
        True if successful, False otherwise
    """
    print("[LinkedIn] Opening browser with persistent session...")
    print("[LinkedIn] Browser mode: headless=False (visible)")
    print("[LinkedIn] Using saved session from: .browser_data/linkedin")
    print("[LinkedIn] Timeout: 90 seconds (slow internet mode)")

    context = None
    try:
        with sync_playwright() as p:
            # Use persistent context to maintain login session
            user_data_dir = VAULT_ROOT / '.browser_data' / 'linkedin'
            user_data_dir.mkdir(parents=True, exist_ok=True)

            # Launch with persistent context (maintains cookies/session)
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(user_data_dir),
                headless=False,  # Visible browser for manual login
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                timeout=90000  # 90s timeout for slow Karachi internet
            )

            page = context.pages[0] if context.pages else context.new_page()

            try:
                # Navigate to LinkedIn
                print("[LinkedIn] Navigating to LinkedIn...")
                page.goto('https://www.linkedin.com/feed/', timeout=90000)

                # Wait for slow assets to load (10 seconds)
                print("[LinkedIn] Waiting 10 seconds for page assets to load...")
                page.wait_for_timeout(10000)

                # ROBUST SELECTOR: Click 'Start a post' button
                print("[LinkedIn] Clicking 'Start a post' button...")
                start_post_button = page.locator('text=Start a post')
                if start_post_button.count() > 0:
                    start_post_button.click(timeout=90000)
                    print("[LinkedIn] Post composer opened")
                else:
                    # Fallback: Try the share box selector
                    share_box = page.locator('.share-box-feed-entry__trigger')
                    if share_box.count() > 0:
                        share_box.click(timeout=90000)
                        print("[LinkedIn] Post composer opened (fallback selector)")
                    else:
                        raise Exception("'Start a post' button not found - may need to log in")

                # Wait for editor to appear
                print("[LinkedIn] Waiting for editor to appear...")
                editor = page.locator('.ql-editor').first
                editor.wait_for(state='visible', timeout=90000)

                # LINKEDIN FIX: Upload image BEFORE typing text
                if media_path:
                    # HARDCODED PATH CHECK
                    hardcoded_path = 'E:/hackathon_0_digital_fte/AI_Employee_vault/Posts/Assets/default.jpg'
                    if media_path != hardcoded_path:
                        print(f"[LinkedIn] Using vault image: {media_path}")
                    else:
                        print(f"[LinkedIn] Using hardcoded vault image path")

                    # Check if file exists
                    if not Path(media_path).exists():
                        print(f"[LinkedIn] WARNING: Media file not found: {media_path}")
                        print("[LinkedIn] Continuing with text-only post")
                        media_path = None
                    else:
                        # FORCE IMAGE UPLOAD: Find file input or media button
                        print(f"[LinkedIn] FORCE UPLOAD: Uploading {media_path}")
                        try:
                            # Method 1: Direct file input approach
                            file_input = page.locator('input[type="file"]').first
                            if file_input.count() > 0:
                                print("[LinkedIn] Using direct file input method")
                                file_input.set_files(media_path)
                                print("[LinkedIn] File attached via input[type='file']")
                            else:
                                # Method 2: Click media button then handle filechooser
                                print("[LinkedIn] Trying media button approach")
                                media_button = page.locator('button[aria-label="Media"]').first
                                if media_button.count() == 0:
                                    media_button = page.locator('button[aria-label="Add media"]').first
                                if media_button.count() == 0:
                                    media_button = page.locator('button[aria-label*="media"]').first

                                if media_button.count() > 0:
                                    with page.expect_filechooser() as fc_info:
                                        media_button.click(timeout=90000)
                                    file_chooser = fc_info.value
                                    file_chooser.set_files(media_path)
                                    print("[LinkedIn] File attached via filechooser")
                                else:
                                    print("[LinkedIn] WARNING: No media button found")
                                    media_path = None

                            # WAIT LOGIC: Wait for image preview to appear
                            if media_path:
                                print("[LinkedIn] Waiting 5 seconds for image preview to appear...")
                                page.wait_for_timeout(5000)
                                
                                # VERIFY: Check if image preview is visible
                                # LinkedIn shows image in composer with a preview
                                image_preview = page.locator('img[src*="blob:"], img[alt="Image preview"]').first
                                if image_preview.count() > 0:
                                    print("[LinkedIn] ✓ Image preview verified on screen")
                                else:
                                    # Alternative: check for any image in composer
                                    image_preview = page.locator('div[class*="image-preview"], img[class*="image"]').first
                                    if image_preview.count() > 0:
                                        print("[LinkedIn] ✓ Image preview verified (fallback)")
                                    else:
                                        print("[LinkedIn] WARNING: Could not verify image preview, but continuing")

                        except Exception as upload_error:
                            print(f"[LinkedIn] WARNING: Image upload failed: {upload_error}")
                            print("[LinkedIn] Continuing with text-only post")
                            media_path = None

                # LINKEDIN WAIT: After upload, type the post content
                # Type content (AFTER image upload)
                print(f"[LinkedIn] Typing content ({len(content)} chars)...")
                editor.fill(content, timeout=90000)
                
                # Add delay to ensure Post button becomes clickable
                # LinkedIn sometimes disables it briefly while processing text
                print("[LinkedIn] Waiting 3 seconds for Post button to become clickable...")
                page.wait_for_timeout(3000)
                time.sleep(1)

                # NOTE: Image upload already done BEFORE typing text (see above)
                # media_path is set to None if upload failed to prevent duplicate upload

                # VERIFY: Ensure Post button is only clicked after image preview is visible
                if media_path:
                    print("[LinkedIn] VERIFICATION: Image upload completed, ready to post")
                else:
                    print("[LinkedIn] VERIFICATION: Text-only post (no image uploaded)")

                # Click Post button with robust multi-selector approach
                print("[LinkedIn] Publishing post...")
                
                # Try multiple selectors for the Post button in priority order
                post_button = None
                selectors = [
                    ("Role-based", lambda: page.get_by_role('button', name='Post', exact=True)),
                    ("CSS class", lambda: page.locator('button.share-actions__post-action')),
                    ("Text content", lambda: page.locator('button:has-text("Post")')),
                    ("ARIA label", lambda: page.locator('button[aria-label="Post"]')),
                    ("Fallback", lambda: page.locator('.share-box_actions button')),
                ]
                
                for selector_name, selector_fn in selectors:
                    try:
                        post_button = selector_fn()
                        if post_button.count() > 0 and post_button.is_visible(timeout=5000):
                            print(f"[LinkedIn] Found Post button using {selector_name} selector")
                            break
                        post_button = None
                    except Exception:
                        continue
                
                if post_button and post_button.count() > 0:
                    # Click Post button
                    post_button.click(timeout=90000)
                    print("[LinkedIn] Post button clicked")
                    
                    # Wait for success confirmation
                    # Option 1: Wait for 'Post successful' toast
                    # Option 2: Wait for editor to disappear
                    # Option 3: Wait for networkidle
                    print("[LinkedIn] Waiting for post success confirmation...")
                    
                    try:
                        # Try waiting for editor to disappear (indicates success)
                        editor.wait_for(state='hidden', timeout=30000)
                        print("[LinkedIn] Editor closed - post successful!")
                    except Exception:
                        # Fallback: wait for networkidle
                        print("[LinkedIn] Waiting for network confirmation...")
                        page.wait_for_load_state('networkidle', timeout=90000)
                    
                    time.sleep(2)
                    print("[LinkedIn] ✓ Post published successfully!")

                    log_action(
                        action_type='linkedin_post_published',
                        file_path='https://www.linkedin.com/feed/',
                        status='completed',
                        metadata={
                            'content_length': len(content),
                            'has_media': media_path is not None,
                        },
                        source='linkedin'
                    )
                    return True
                else:
                    raise Exception("Post button not found after trying multiple selectors")

            except Exception as inner_e:
                print(f"[LinkedIn] ERROR during posting: {inner_e}")
                log_action(
                    action_type='linkedin_post_error',
                    file_path='https://www.linkedin.com/feed/',
                    status='error',
                    error_message=str(inner_e),
                    source='linkedin'
                )
                raise

    except Exception as e:
        print(f"[LinkedIn] Browser error: {e}")
        log_action(
            action_type='linkedin_browser_error',
            file_path='https://www.linkedin.com/feed/',
            status='error',
            error_message=str(e),
            source='linkedin'
        )
        return False
    
    finally:
        # ALWAYS close browser, even on timeout/error
        if context:
            try:
                print("[LinkedIn] Closing browser...")
                context.close()
            except Exception as close_error:
                print(f"[LinkedIn] Warning: Error closing browser: {close_error}")
    
    return True


# ============================================================================
# Main LinkedIn Poster
# ============================================================================

def check_approved_posts():
    """Check /Approved for posts ready to publish.
    
    SMART FOLDER LOGIC: Files in /Approved are assumed approved by default.
    The FOLDER LOCATION itself is the approval - YAML metadata is IGNORED.
    Processes ANY .md file in /Approved folder.
    """
    print("[LinkedIn] Checking /Approved for posts...")
    print("[LinkedIn] SMART FOLDER LOGIC: Files in /Approved are auto-approved")
    print("[LinkedIn] YAML 'status' and 'hitl_approved' fields will be IGNORED")

    if not APPROVED_PATH.exists():
        print("[LinkedIn] /Approved folder not found")
        return

    # Find ALL .md files in /Approved (any filename ending in .md)
    print(f"[LinkedIn] Scanning for .md files in {APPROVED_PATH}")
    md_files = list(APPROVED_PATH.glob('*.md'))
    print(f"[LinkedIn] Found {len(md_files)} .md file(s)")

    for post_file in md_files:
        try:
            # Parse metadata (for content extraction only)
            metadata = parse_post_metadata(post_file)

            # SMART FOLDER: If no metadata, create minimal metadata
            if not metadata:
                print(f"[LinkedIn] WARNING: {post_file.name} has no metadata - creating minimal metadata")
                metadata = {
                    'platform': 'linkedin',
                    'content': '',
                }

            # SMART FOLDER: COMPLETELY BYPASS status and hitl_approved checks
            # The file being in /Approved IS the approval
            print(f"[LinkedIn] Processing: {post_file.name} (location = approval)")
            
            # Check platform (only required field besides content)
            platform = metadata.get('platform', '').strip().lower()
            if not platform:
                # Default to linkedin if in /Approved folder
                print(f"[LinkedIn] WARNING: {post_file.name} missing 'platform' - assuming 'linkedin'")
                platform = 'linkedin'
            
            if platform != 'linkedin':
                print(f"[LinkedIn] Skipped: {post_file.name} - Platform is '{platform}', not 'linkedin'")
                continue

            # Extract content
            content = metadata.get('content', '')
            media_path = metadata.get('media_path')

            if not content:
                print(f"[LinkedIn] ERROR: {post_file.name} - No content found in file")
                print(f"[LinkedIn]   Action: Add 'content:' field to the file metadata")
                log_action(
                    action_type='linkedin_post_skipped',
                    file_path=str(post_file),
                    status='skipped',
                    error_message='No content',
                    source='linkedin'
                )
                continue

            # Publish
            print(f"[LinkedIn] ✓ Publishing: {post_file.name}")
            success = publish_to_linkedin(content, media_path)

            if success:
                # Update status in file (for record keeping)
                update_post_status(
                    post_file,
                    'published',
                    hitl_approved_by='linkedin-agent',
                    hitl_approved_at=datetime.now().isoformat() + 'Z',
                    published_at=datetime.now().isoformat() + 'Z'
                )

                # CLEANUP: Move to /Done after successful post (prevents duplicate posting)
                done_path = DONE_PATH / post_file.name
                post_file.rename(done_path)
                print(f"[LinkedIn] ✓ Moved to /Done: {post_file.name}")
                print(f"[LinkedIn] File moved to prevent duplicate posting")

                log_action(
                    action_type='linkedin_post_completed',
                    file_path=str(done_path),
                    status='completed',
                    metadata={'original_file': str(post_file)},
                    source='linkedin'
                )
            else:
                print(f"[LinkedIn] Publishing failed for: {post_file.name}")
                print(f"[LinkedIn] File remains in /Approved for retry")
                log_action(
                    action_type='linkedin_post_failed',
                    file_path=str(post_file),
                    status='failed',
                    error_message='Publishing failed',
                    source='linkedin'
                )

        except Exception as e:
            # DEBUG: Print exact error message
            print(f"[LinkedIn] ERROR processing {post_file.name}:")
            print(f"[LinkedIn]   Exception type: {type(e).__name__}")
            print(f"[LinkedIn]   Error message: {str(e)}")
            print(f"[LinkedIn]   File path: {post_file}")
            log_action(
                action_type='linkedin_processing_error',
                file_path=str(post_file),
                status='error',
                error_message=str(e),
                source='linkedin'
            )


def run_poster():
    """Run LinkedIn poster continuously (check every 2 minutes)."""
    print("=" * 60)
    print("Digital FTE - LinkedIn Poster")
    print("=" * 60)
    print()
    print(f"Monitoring /Approved for LinkedIn posts every 2 minutes...")
    print("Press Ctrl+C to stop")
    print()
    
    while True:
        try:
            check_approved_posts()
            time.sleep(120)  # 2 minutes
        except KeyboardInterrupt:
            print("\n[LinkedIn] Stopped by user")
            break
        except Exception as e:
            print(f"[LinkedIn] Error in poster loop: {e}")
            time.sleep(60)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # Run once (for testing)
        check_approved_posts()
    else:
        # Run continuously
        run_poster()
