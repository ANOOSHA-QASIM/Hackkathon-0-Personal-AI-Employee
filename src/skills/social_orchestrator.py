"""
Social Orchestrator - Master dispatcher for multi-platform social media posting.

Scans /Approved/Social/ for post files and triggers LinkedIn, Meta, and Twitter skills.
Logs all actions to /Logs/social_audit.json with timestamps.
"""

import os
import sys
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List

# Paths
VAULT_ROOT = Path(os.environ.get('VAULT_ROOT', 'E:/hackathon_0_digital_fte/AI_Employee_vault'))
APPROVED_SOCIAL_PATH = VAULT_ROOT / 'Approved' / 'Social'
DONE_SOCIAL_PATH = VAULT_ROOT / 'Done' / 'Social'
LOGS_PATH = VAULT_ROOT / 'Logs'

# Import skills
sys.path.insert(0, str(VAULT_ROOT / 'src'))
from skills.meta_poster import MetaPoster
from skills.twitter_poster import TwitterPoster
from skills.odoo_manager import OdooManager
from linkedin.linkedin_poster import publish_to_linkedin
# LinkedIn poster imported from Phase 2 (function-based API)

# Initialize Odoo Manager (lazy initialization on first use)
_odoo_manager = None


def get_odoo_manager() -> OdooManager:
    """Get or create Odoo Manager instance."""
    global _odoo_manager
    if _odoo_manager is None:
        _odoo_manager = OdooManager()
    return _odoo_manager


def parse_frontmatter(file_path: Path) -> Dict:
    """Parse YAML frontmatter from Markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if not content.startswith('---'):
        return {}

    end = content.find('---', 3)
    if end == -1:
        return {}

    yaml_content = content[3:end].strip()

    try:
        import yaml
        return yaml.safe_load(yaml_content)
    except:
        return {}


def log_social_action(platform: str, post_file: str, status: str, error: str = None):
    """Log social media action to /Logs/social_audit.json."""
    LOGS_PATH.mkdir(parents=True, exist_ok=True)
    log_path = LOGS_PATH / 'social_audit.json'

    # Load or initialize log
    if log_path.exists():
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
        except:
            log_data = {'entries': []}
    else:
        log_data = {'entries': []}

    # Create log entry
    entry = {
        'timestamp': datetime.now().isoformat(),
        'platform': platform,
        'post_file': post_file,
        'status': status,
    }

    if error:
        entry['error'] = error

    log_data['entries'].append(entry)

    # Write log
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2)

    print(f"[Audit] Logged: {platform} - {status}")


def process_post_file(post_file: Path) -> Dict[str, bool]:
    """
    Process a single post file across all platforms.

    Args:
        post_file: Path to post file in /Approved/Social/

    Returns:
        Dictionary of platform -> success status
    """
    print(f"\n[Orchestrator] Processing: {post_file.name}")

    # Parse metadata
    metadata = parse_frontmatter(post_file)
    content = metadata.get('content', '')
    media_path = metadata.get('media_path')

    if not content:
        print(f"[Orchestrator] ERROR: No content in {post_file.name}")
        return {}

    results = {}

    # ERROR HANDLING: Wrap each platform call in try/except so one platform's crash doesn't stop the whole script
    
    # 1. LinkedIn (Phase 2 integration)
    print("\n[Orchestrator] === LinkedIn ===")
    try:
        # LinkedIn uses function-based API - returns True/False
        result = publish_to_linkedin(content, media_path)
        
        # Convert result to boolean (handles both bool and truthy values)
        linkedin_success = bool(result)
        results['linkedin'] = linkedin_success
        
        # Log action
        status = 'published' if linkedin_success else 'failed'
        log_social_action('linkedin', post_file.name, status)
        print(f"[Orchestrator] LinkedIn result: {status}")

        # AUTO-LOG: Log expense to Odoo after successful post
        if linkedin_success:
            try:
                odoo = get_odoo_manager()
                odoo_result = odoo.log_post_expense(platform='linkedin', post_title=post_file.stem)
                if odoo_result:
                    print(f"[Orchestrator] ✓ Odoo expense logged - Move ID: {odoo_result.get('move_id')}")
                else:
                    print("[Orchestrator] ⚠ Odoo logging skipped (connection failed)")
            except Exception as odoo_error:
                print(f"[Orchestrator] ⚠ Odoo logging failed: {odoo_error}")
    except ImportError:
        print("[Orchestrator] LinkedIn module not available (Phase 2 may not be complete)")
        results['linkedin'] = False
        log_social_action('linkedin', post_file.name, 'skipped', 'Module not available')
    except Exception as e:
        print(f"[Orchestrator] LinkedIn ERROR: {e}")
        results['linkedin'] = False
        log_social_action('linkedin', post_file.name, 'failed', str(e))

    # 2. Meta (Facebook) - ERROR HANDLING: Wrapped in try/except
    print("\n[Orchestrator] === Meta (Facebook) ===")
    try:
        meta = MetaPoster()
        # Pass post_file path so meta_poster can move file to /Done after success
        metadata['_post_file_path'] = str(post_file)
        result = meta.post(content, media_path, metadata)  # Pass metadata with post_file_path
        results['meta'] = (result.status == 'published')
        log_social_action('meta', post_file.name, result.status, result.error)
        print(f"[Orchestrator] Meta result: {result.status}")
        
        # AUTO-LOG: Log expense to Odoo after successful post
        if result.status == 'published':
            try:
                odoo = get_odoo_manager()
                odoo_result = odoo.log_post_expense(platform='facebook', post_title=post_file.stem)
                if odoo_result:
                    print(f"[Orchestrator] ✓ Odoo expense logged - Move ID: {odoo_result.get('move_id')}")
                else:
                    print("[Orchestrator] ⚠ Odoo logging skipped (connection failed)")
            except Exception as odoo_error:
                print(f"[Orchestrator] ⚠ Odoo logging failed: {odoo_error}")
    except Exception as e:
        print(f"[Orchestrator] Meta ERROR: {e}")
        results['meta'] = False
        log_social_action('meta', post_file.name, 'failed', str(e))

    # 3. Twitter (X) - ERROR HANDLING: Wrapped in try/except
    print("\n[Orchestrator] === Twitter (X) ===")
    try:
        twitter = TwitterPoster()
        result = twitter.post(content, media_path)  # FIX TWITTER CRASH: Ensure correct arguments (content, media_path)
        results['twitter'] = (result.status == 'published')
        log_social_action('twitter', post_file.name, result.status, result.error)
        print(f"[Orchestrator] Twitter result: {result.status}")
        
        # AUTO-LOG: Log expense to Odoo after successful post
        if result.status == 'published':
            try:
                odoo = get_odoo_manager()
                odoo_result = odoo.log_post_expense(platform='twitter', post_title=post_file.stem)
                if odoo_result:
                    print(f"[Orchestrator] ✓ Odoo expense logged - Move ID: {odoo_result.get('move_id')}")
                else:
                    print("[Orchestrator] ⚠ Odoo logging skipped (connection failed)")
            except Exception as odoo_error:
                print(f"[Orchestrator] ⚠ Odoo logging failed: {odoo_error}")
    except Exception as e:
        print(f"[Orchestrator] Twitter ERROR: {e}")
        results['twitter'] = False
        log_social_action('twitter', post_file.name, 'failed', str(e))

    return results


def scan_approved_social():
    """Scan /Approved/Social/ for post files to process."""
    print("=" * 60)
    print("Social Media Orchestrator")
    print("=" * 60)
    print()

    # Ensure directories exist
    APPROVED_SOCIAL_PATH.mkdir(parents=True, exist_ok=True)
    DONE_SOCIAL_PATH.mkdir(parents=True, exist_ok=True)

    # Find all .md files in /Approved/Social/
    post_files = list(APPROVED_SOCIAL_PATH.glob('*.md'))

    if not post_files:
        print("[Orchestrator] No posts found in /Approved/Social/")
        return

    print(f"[Orchestrator] Found {len(post_files)} post(s) to process")
    print()

    # Process each file
    for post_file in post_files:
        results = process_post_file(post_file)

        # Check if all platforms succeeded
        all_success = all(results.values()) if results else False

        if all_success:
            # Move to /Done/Social/ using shutil.move for Windows compatibility
            done_path = DONE_SOCIAL_PATH / post_file.name
            try:
                shutil.move(str(post_file), str(done_path))
                print(f"\n[Orchestrator] ✓ Moved to /Done: {post_file.name}")
            except Exception as move_error:
                print(f"\n[Orchestrator] ⚠ Could not move file to /Done: {move_error}")
                print(f"[Orchestrator] File remains in /Approved")
        else:
            print(f"\n[Orchestrator] ⚠ Some platforms failed, file remains in /Approved")
            print(f"   Results: {results}")


def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # Run once
        scan_approved_social()
    else:
        # Run continuously (check every 2 minutes)
        print("[Orchestrator] Running continuously (check every 2 minutes)...")
        print("[Orchestrator] Press Ctrl+C to stop")
        print()

        while True:
            try:
                scan_approved_social()
                import time
                time.sleep(120)  # 2 minutes
            except KeyboardInterrupt:
                print("\n[Orchestrator] Stopped by user")
                break
            except Exception as e:
                print(f"[Orchestrator] ERROR: {e}")
                import time
                time.sleep(60)


if __name__ == '__main__':
    main()
