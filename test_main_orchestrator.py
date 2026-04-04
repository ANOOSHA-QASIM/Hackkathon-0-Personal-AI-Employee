"""
Test Decoupled Master Orchestrator

Verifies main.py only contains Social Media + Odoo workflows (no Gmail).
"""

import sys
from pathlib import Path

# Vault root
VAULT_ROOT = Path(__file__).parent


def test_script_paths():
    """Test that required script paths exist."""
    print("=" * 60)
    print("Decoupled Master Orchestrator Test")
    print("=" * 60)
    print()

    scripts = {
        'social_orchestrator': VAULT_ROOT / 'src' / 'skills' / 'social_orchestrator.py',
        'ceo_briefer': VAULT_ROOT / 'src' / 'skills' / 'ceo_briefer.py',
    }

    print("[Test 1] Verifying script paths...")
    all_exist = True

    for name, path in scripts.items():
        exists = path.exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {name:25} {path.name}")
        if not exists:
            all_exist = False

    return all_exist


def test_no_gmail_references():
    """Test that main.py has no Gmail-related code."""
    print()
    print("[Test 2] Verifying no Gmail references...")

    try:
        with open(VAULT_ROOT / 'main.py', 'r', encoding='utf-8') as f:
            content = f.read()

        gmail_terms = ['gmail_monitor', 'auto_drafter', 'gmail_sender', 'GmailMonitor', 'AutoDrafter', 'GmailSender']
        found_gmail = []

        for term in gmail_terms:
            if term.lower() in content.lower():
                found_gmail.append(term)

        if found_gmail:
            print(f"  ✗ Found Gmail references: {', '.join(found_gmail)}")
            return False
        else:
            print("  ✓ No Gmail references found")
            return True

    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        return False


def test_has_social_and_ceo():
    """Test that main.py has Social Orchestrator and CEO Briefer."""
    print()
    print("[Test 3] Verifying Social + CEO workflows...")

    try:
        with open(VAULT_ROOT / 'main.py', 'r', encoding='utf-8') as f:
            content = f.read()

        checks = {
            'social_orchestrator': 'social_orchestrator' in content.lower(),
            'ceo_briefer': 'ceo_briefer' in content.lower(),
            'odoo_logging': 'odoo' in content.lower() or 'expense' in content.lower(),
            '5-minute interval': 'LOOP_INTERVAL = 300' in content,
            'while True loop': 'while True:' in content,
            'error handling': 'except Exception' in content,
        }

        all_pass = True
        for check, result in checks.items():
            status = "✓" if result else "✗"
            print(f"  {status} {check}")
            if not result:
                all_pass = False

        return all_pass

    except Exception as e:
        print(f"  ✗ Test failed: {e}")
        return False


def test_main_import():
    """Test that main.py can be imported."""
    print()
    print("[Test 4] Testing main.py import...")

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("main", VAULT_ROOT / 'main.py')
        main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_module)

        assert hasattr(main_module, 'run_script'), "Missing run_script function"
        assert hasattr(main_module, 'run_cycle'), "Missing run_cycle function"
        assert hasattr(main_module, 'main'), "Missing main function"

        print("✓ main.py imported successfully")
        print("✓ run_script function exists")
        print("✓ run_cycle function exists")
        print("✓ main function exists")

        return True

    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False


def main():
    """Run all tests."""
    print()

    # Test 1: Script paths
    test1 = test_script_paths()

    # Test 2: No Gmail
    test2 = test_no_gmail_references()

    # Test 3: Has Social + CEO
    test3 = test_has_social_and_ceo()

    # Test 4: Import
    test4 = test_main_import()

    # Summary
    print()
    print("=" * 60)
    print("Decoupled Master Orchestrator Test Results")
    print("=" * 60)
    print(f"Script Paths:      {'✓ PASS' if test1 else '✗ FAIL'}")
    print(f"No Gmail Code:     {'✓ PASS' if test2 else '✗ FAIL'}")
    print(f"Social + CEO:      {'✓ PASS' if test3 else '✗ FAIL'}")
    print(f"Module Import:     {'✓ PASS' if test4 else '✗ FAIL'}")
    print()

    if test1 and test2 and test3 and test4:
        print("🎉 DECOUPLED MASTER ORCHESTRATOR COMPLETE!")
        print()
        print("What was updated:")
        print("  ✓ main.py - Social Media + Odoo only")
        print("  ✓ Removed: Gmail Monitor, Auto-Drafter, Gmail Sender")
        print("  ✓ Kept: Social Orchestrator, CEO Briefer")
        print("  ✓ 5-minute cycle interval")
        print("  ✓ Odoo logging for LinkedIn, Meta, Twitter")
        print()
        print("Run Master Orchestrator:")
        print("  python main.py")
        print()
        print("What happens each cycle:")
        print("  1. Social Orchestrator - Post approved content → Odoo")
        print("  2. CEO Briefer - Update daily report → CEO_Report.md")
        print()
        return True
    else:
        print("⚠ Some tests failed")
        print()
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
