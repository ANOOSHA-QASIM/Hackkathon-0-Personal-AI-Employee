"""
Test Unified Master Orchestrator

Verifies the main.py orchestrator structure and script paths.
"""

import sys
from pathlib import Path

# Vault root
VAULT_ROOT = Path(__file__).parent


def test_script_paths():
    """Test that all script paths exist."""
    print("=" * 60)
    print("Unified Master Orchestrator Test")
    print("=" * 60)
    print()

    scripts = {
        'gmail_monitor': VAULT_ROOT / 'src' / 'gmail' / 'gmail_monitor.py',
        'auto_drafter': VAULT_ROOT / 'src' / 'agent' / 'auto_drafter.py',
        'social_orchestrator': VAULT_ROOT / 'src' / 'skills' / 'social_orchestrator.py',
        'gmail_sender': VAULT_ROOT / 'src' / 'gmail' / 'gmail_sender.py',
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


def test_main_import():
    """Test that main.py can be imported."""
    print()
    print("[Test 2] Testing main.py import...")

    try:
        # Import main module
        import importlib.util
        spec = importlib.util.spec_from_file_location("main", VAULT_ROOT / 'main.py')
        main_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(main_module)

        # Check for required functions
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


def test_loop_structure():
    """Test the loop structure."""
    print()
    print("[Test 3] Testing loop structure...")

    try:
        # Check main.py content
        with open(VAULT_ROOT / 'main.py', 'r', encoding='utf-8') as f:
            content = f.read()

        # Verify key components
        checks = {
            'while True loop': 'while True:' in content,
            '5-minute delay': 'LOOP_INTERVAL = 300' in content,
            'Gmail Monitor': 'gmail_monitor' in content,
            'Auto-Drafter': 'auto_drafter' in content,
            'Social Orchestrator': 'social_orchestrator' in content,
            'Gmail Sender': 'gmail_sender' in content,
            'CEO Briefer': 'ceo_briefer' in content,
            'Error handling': 'except Exception' in content,
            'Ctrl+C handling': 'KeyboardInterrupt' in content,
        }

        all_pass = True
        for check, result in checks.items():
            status = "✓" if result else "✗"
            print(f"  {status} {check}")
            if not result:
                all_pass = False

        return all_pass

    except Exception as e:
        print(f"✗ Structure test failed: {e}")
        return False


def main():
    """Run all tests."""
    print()

    # Test 1: Script paths
    test1 = test_script_paths()

    # Test 2: Import
    test2 = test_main_import()

    # Test 3: Loop structure
    test3 = test_loop_structure()

    # Summary
    print()
    print("=" * 60)
    print("Master Orchestrator Test Results")
    print("=" * 60)
    print(f"Script Paths:    {'✓ PASS' if test1 else '✗ FAIL'}")
    print(f"Module Import:   {'✓ PASS' if test2 else '✗ FAIL'}")
    print(f"Loop Structure:  {'✓ PASS' if test3 else '✗ FAIL'}")
    print()

    if test1 and test2 and test3:
        print("🎉 UNIFIED MASTER ORCHESTRATOR COMPLETE!")
        print()
        print("What was created:")
        print("  ✓ main.py - Continuous automation loop")
        print("  ✓ Sequences: Gmail → Drafts → Social → Send → CEO Report")
        print("  ✓ 5-minute cycle interval")
        print("  ✓ Error isolation (one failure doesn't stop others)")
        print("  ✓ Graceful shutdown (Ctrl+C)")
        print()
        print("Run Master Orchestrator:")
        print("  python main.py")
        print()
        print("What happens each cycle:")
        print("  1. Gmail Monitor - Fetch new emails → /Needs_Action")
        print("  2. Auto-Drafter - Generate AI replies → /In_Progress")
        print("  3. Social Orchestrator - Post approved content → Odoo")
        print("  4. Gmail Sender - Send approved replies → Gmail")
        print("  5. CEO Briefer - Update daily report → CEO_Report.md")
        print()
        return True
    else:
        print("⚠ Some tests failed")
        print()
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
