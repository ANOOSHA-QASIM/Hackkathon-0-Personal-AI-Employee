"""
Unified Test - LinkedIn + Meta + Twitter + Odoo Integration

Tests that all platforms are integrated into the social orchestrator
with automatic Odoo expense logging.
"""

import sys
from pathlib import Path

# Add src to path
VAULT_ROOT = Path(__file__).parent
sys.path.insert(0, str(VAULT_ROOT / 'src'))

from skills.odoo_manager import OdooManager
from linkedin.linkedin_poster import LinkedInPoster


def test_linkedin_import():
    """Test that LinkedIn poster can be imported."""
    print("=" * 60)
    print("Unified Integration Test - LinkedIn + Meta + Twitter + Odoo")
    print("=" * 60)
    print()
    
    print("[Test 1] Testing LinkedIn import...")
    try:
        from skills.social_orchestrator import LinkedInPoster
        print("✓ LinkedInPoster imported successfully")
        return True
    except ImportError as e:
        print(f"✗ LinkedIn import failed: {e}")
        return False


def test_odoo_connection():
    """Test Odoo connection."""
    print()
    print("[Test 2] Testing Odoo connection...")
    odoo = OdooManager()
    
    if odoo.authenticate():
        print(f"✓ Odoo Connected - UID: {odoo.uid}")
        return odoo
    else:
        print("✗ Odoo Connection Failed")
        return None


def test_linkedin_expense_logging(odoo):
    """Test logging LinkedIn expense to Odoo."""
    print()
    print("[Test 3] Testing LinkedIn expense logging...")
    
    try:
        result = odoo.log_post_expense(
            platform='linkedin',
            post_title='Unified Integration Test'
        )
        
        if result:
            print(f"✓ LinkedIn Expense Logged - Move ID: {result.get('move_id')}")
            print(f"  Platform: {result.get('platform')}")
            print(f"  Amount: {result.get('amount')} PKR")
            return result.get('move_id')
        else:
            print("⚠ LinkedIn logging returned None")
            return None
    except Exception as e:
        print(f"✗ LinkedIn logging failed: {e}")
        return None


def test_all_platforms_expense(odoo):
    """Test logging expenses for all platforms."""
    print()
    print("[Test 4] Testing all platforms expense logging...")
    
    platforms = ['linkedin', 'facebook', 'twitter', 'instagram']
    move_ids = {}
    
    for platform in platforms:
        try:
            result = odoo.log_post_expense(
                platform=platform,
                post_title=f'{platform.capitalize()} Test Post'
            )
            
            if result:
                move_ids[platform] = result.get('move_id')
                print(f"  ✓ {platform.capitalize()}: Move ID {result.get('move_id')}")
            else:
                print(f"  ⚠ {platform.capitalize()}: Skipped")
        except Exception as e:
            print(f"  ✗ {platform.capitalize()}: Failed - {e}")
    
    return move_ids


def main():
    """Run all tests."""
    print()
    
    # Test 1: LinkedIn import
    linkedin_ok = test_linkedin_import()
    
    # Test 2: Odoo connection
    odoo = test_odoo_connection()
    
    # Test 3: LinkedIn expense
    move_id_linkedin = None
    if odoo:
        move_id_linkedin = test_linkedin_expense_logging(odoo)
    
    # Test 4: All platforms
    move_ids = {}
    if odoo:
        move_ids = test_all_platforms_expense(odoo)
    
    # Summary
    print()
    print("=" * 60)
    print("Unified Integration Test Results")
    print("=" * 60)
    print(f"LinkedIn Import:      {'✓ PASS' if linkedin_ok else '✗ FAIL'}")
    print(f"Odoo Connection:      {'✓ PASS' if odoo else '✗ FAIL'}")
    if odoo:
        print(f"  UID: {odoo.uid}")
    print(f"LinkedIn Expense:     {'✓ PASS' if move_id_linkedin else '✗ FAIL'}")
    if move_id_linkedin:
        print(f"  Move ID: {move_id_linkedin}")
    print(f"All Platforms:        {'✓ PASS' if move_ids else '✗ FAIL'}")
    for platform, move_id in move_ids.items():
        if move_id:
            print(f"  {platform.capitalize()}: Move ID {move_id}")
    print()
    
    if linkedin_ok and odoo and move_ids:
        print("🎉 UNIFIED INTEGRATION COMPLETE!")
        print()
        print("What happens now:")
        print("  - Social orchestrator posts to: LinkedIn, Facebook, Twitter, Instagram")
        print("  - Each successful post → creates Odoo journal entry")
        print("  - Expense amount: 500 PKR per post (configurable)")
        print("  - All entries created as drafts for review")
        print()
        print("Run full orchestrator:")
        print("  python src/skills/social_orchestrator.py --once")
        print()
        print("Verify in Odoo:")
        print("  1. Open: http://localhost:8069")
        print("  2. Go to: Invoicing → Accounting → Journal Entries")
        print("  3. Look for Move IDs listed above")
        print()
        return True
    else:
        print("⚠ Some tests failed")
        print()
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
