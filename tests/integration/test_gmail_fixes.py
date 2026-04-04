"""
Test Gmail Monitor Fixes

Run this to verify the bug fixes work correctly.

Usage:
    python tests/integration/test_gmail_fixes.py
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from gmail.gmail_monitor import (
    load_processed_emails,
    save_processed_email,
    log_action,
    LOGS_PATH,
    PROCESSED_EMAILS_PATH
)


def test_load_processed_emails_empty_file():
    """Test: load_processed_emails handles empty file."""
    print()
    print("=" * 60)
    print("Test: load_processed_emails with empty file")
    print("=" * 60)
    print()
    
    # Create empty file
    PROCESSED_EMAILS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(PROCESSED_EMAILS_PATH, 'w', encoding='utf-8') as f:
        f.write('')
    
    # Should return empty set, not crash
    result = load_processed_emails()
    
    if isinstance(result, set):
        print("✓ PASS: load_processed_emails returned empty set for empty file")
        return True
    else:
        print(f"✗ FAIL: Expected set, got {type(result)}")
        return False


def test_load_processed_emails_invalid_json():
    """Test: load_processed_emails handles invalid JSON."""
    print()
    print("=" * 60)
    print("Test: load_processed_emails with invalid JSON")
    print("=" * 60)
    print()
    
    # Create file with invalid JSON
    with open(PROCESSED_EMAILS_PATH, 'w', encoding='utf-8') as f:
        f.write('invalid json {')
    
    # Should return empty set, not crash
    result = load_processed_emails()
    
    if isinstance(result, set):
        print("✓ PASS: load_processed_emails handled invalid JSON gracefully")
        return True
    else:
        print(f"✗ FAIL: Expected set, got {type(result)}")
        return False


def test_load_processed_emails_missing_file():
    """Test: load_processed_emails creates file if missing."""
    print()
    print("=" * 60)
    print("Test: load_processed_emails with missing file")
    print("=" * 60)
    print()
    
    # Delete file if exists
    if PROCESSED_EMAILS_PATH.exists():
        PROCESSED_EMAILS_PATH.unlink()
    
    # Should create file and return empty set
    result = load_processed_emails()
    
    if isinstance(result, set) and PROCESSED_EMAILS_PATH.exists():
        print("✓ PASS: load_processed_emails created missing file")
        return True
    else:
        print(f"✗ FAIL: Expected set and file creation")
        return False


def test_log_action_with_kwargs():
    """Test: log_action accepts kwargs."""
    print()
    print("=" * 60)
    print("Test: log_action with kwargs")
    print("=" * 60)
    print()
    
    try:
        # Should accept source and other kwargs without TypeError
        log_action(
            action_type='test_action',
            file_path='/test/path',
            status='completed',
            metadata={'test': 'data'},
            source='gmail',
            extra_field='extra_value'
        )
        
        # Verify log was created
        today = Path(LOGS_PATH).strftime('%Y-%m-%d')
        log_path = LOGS_PATH / f'{today}.json'
        
        if log_path.exists():
            with open(log_path, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
            
            # Find our test entry
            test_entry = None
            for entry in log_data['entries']:
                if entry.get('action_type') == 'test_action':
                    test_entry = entry
                    break
            
            if test_entry and test_entry.get('source') == 'gmail':
                print("✓ PASS: log_action accepted kwargs and logged correctly")
                return True
            else:
                print("✗ FAIL: log entry not found or missing source field")
                return False
        else:
            print("✗ FAIL: Log file not created")
            return False
            
    except TypeError as e:
        print(f"✗ FAIL: log_action raised TypeError: {e}")
        return False
    except Exception as e:
        print(f"✗ FAIL: Unexpected error: {e}")
        return False


def test_absolute_paths():
    """Test: All paths are absolute."""
    print()
    print("=" * 60)
    print("Test: Absolute paths")
    print("=" * 60)
    print()
    
    from gmail.gmail_monitor import VAULT_ROOT, NEEDS_ACTION_PATH, LOGS_PATH
    
    # Check if paths are absolute
    if VAULT_ROOT.is_absolute():
        print(f"✓ VAULT_ROOT is absolute: {VAULT_ROOT}")
    else:
        print(f"✗ VAULT_ROOT is not absolute: {VAULT_ROOT}")
        return False
    
    if NEEDS_ACTION_PATH.is_absolute():
        print(f"✓ NEEDS_ACTION_PATH is absolute: {NEEDS_ACTION_PATH}")
    else:
        print(f"✗ NEEDS_ACTION_PATH is not absolute: {NEEDS_ACTION_PATH}")
        return False
    
    if LOGS_PATH.is_absolute():
        print(f"✓ LOGS_PATH is absolute: {LOGS_PATH}")
    else:
        print(f"✗ LOGS_PATH is not absolute: {LOGS_PATH}")
        return False
    
    print("✓ PASS: All paths are absolute")
    return True


def run_all_tests():
    """Run all fix verification tests."""
    print("=" * 60)
    print("Gmail Monitor - Bug Fix Verification")
    print("=" * 60)
    
    tests = [
        ("Empty File Handling", test_load_processed_emails_empty_file),
        ("Invalid JSON Handling", test_load_processed_emails_invalid_json),
        ("Missing File Handling", test_load_processed_emails_missing_file),
        ("kwargs Support", test_log_action_with_kwargs),
        ("Absolute Paths", test_absolute_paths),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ {name} failed with exception: {e}")
            results.append((name, False))
    
    # Summary
    print()
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print()
        print("=" * 60)
        print("All Bug Fixes VERIFIED")
        print("=" * 60)
        print()
        print("Next steps:")
        print("1. Run: python src/gmail/gmail_monitor.py --once")
        print("2. Send a test email to your Gmail account")
        print("3. Check /Needs_Action for email alert")
        return True
    else:
        print()
        print("=" * 60)
        print("Some Bug Fixes FAILED")
        print("=" * 60)
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
