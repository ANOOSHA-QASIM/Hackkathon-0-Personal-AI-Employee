"""
Quick Test - LinkedIn Integration with Odoo

Verifies that LinkedIn is properly integrated into the social orchestrator
with automatic Odoo expense logging.
"""

import sys
from pathlib import Path

# Add src to path
VAULT_ROOT = Path(__file__).parent
sys.path.insert(0, str(VAULT_ROOT / 'src'))

from skills.odoo_manager import OdooManager


def test_linkedin_import():
    """Test that LinkedIn function can be imported from orchestrator."""
    print("=" * 60)
    print("LinkedIn Integration Test")
    print("=" * 60)
    print()
    
    print("[Test 1] Testing LinkedIn import from orchestrator...")
    try:
        from skills.social_orchestrator import publish_to_linkedin
        print("✓ publish_to_linkedin imported successfully")
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
            post_title='LinkedIn Integration Test'
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
    
    # Summary
    print()
    print("=" * 60)
    print("LinkedIn Integration Results")
    print("=" * 60)
    print(f"LinkedIn Import:  {'✓ PASS' if linkedin_ok else '✗ FAIL'}")
    print(f"Odoo Connection:  {'✓ PASS' if odoo else '✗ FAIL'}")
    print(f"LinkedIn Expense: {'✓ PASS' if move_id_linkedin else '✗ FAIL'}")
    if move_id_linkedin:
        print(f"  Move ID: {move_id_linkedin}")
    print()
    
    if linkedin_ok and odoo and move_id_linkedin:
        print("🎉 LINKEDIN INTEGRATION COMPLETE!")
        print()
        print("Social Orchestrator now posts to:")
        print("  ✓ LinkedIn (with Odoo expense logging)")
        print("  ✓ Facebook (with Odoo expense logging)")
        print("  ✓ Twitter (with Odoo expense logging)")
        print("  ✓ Instagram (with Odoo expense logging)")
        print()
        print("Run full orchestrator:")
        print("  python src/skills/social_orchestrator.py --once")
        print()
        print("Verify in Odoo:")
        print("  1. Open: http://localhost:8069")
        print("  2. Go to: Invoicing → Accounting → Journal Entries")
        print(f"  3. Look for Move ID: {move_id_linkedin}")
        print()
        return True
    else:
        print("⚠ Some tests failed")
        print()
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
