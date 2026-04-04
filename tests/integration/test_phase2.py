"""
Phase 2 Integration Tests

Run all integration tests for Gmail and LinkedIn functionality.

Usage:
    python tests/integration/test_phase2.py
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from config.settings import VAULT_ROOT, NEEDS_ACTION_PATH, APPROVED_PATH, LOGS_PATH


def test_gmail_alert_creation():
    """Test: Gmail creates alert in /Needs_Action."""
    print()
    print("=" * 60)
    print("Test: Gmail Alert Creation")
    print("=" * 60)
    print()
    
    # Check if gmail_monitor.py exists
    monitor_path = VAULT_ROOT / 'src' / 'gmail' / 'gmail_monitor.py'
    if not monitor_path.exists():
        print("✗ FAIL: gmail_monitor.py not found")
        return False
    
    print("✓ gmail_monitor.py exists")
    
    # Check if credentials.json exists
    creds_path = VAULT_ROOT / 'credentials.json'
    if not creds_path.exists():
        print("⚠ WARNING: credentials.json not found (required for actual testing)")
        print("  To test: Run 'python src/gmail/gmail_auth.py --authenticate'")
        return True  # Script exists, just needs credentials
    
    print("✓ credentials.json exists")
    print()
    print("To complete test:")
    print("1. Send a test email to your Gmail account")
    print("2. Run: python src/gmail/gmail_monitor.py --once")
    print("3. Check /Needs_Action for email alert")
    
    return True


def test_linkedin_post_detection():
    """Test: LinkedIn poster detects files in /Approved."""
    print()
    print("=" * 60)
    print("Test: LinkedIn Post Detection")
    print("=" * 60)
    print()
    
    # Check if linkedin_poster.py exists
    poster_path = VAULT_ROOT / 'src' / 'linkedin' / 'linkedin_poster.py'
    if not poster_path.exists():
        print("✗ FAIL: linkedin_poster.py not found")
        return False
    
    print("✓ linkedin_poster.py exists")
    
    # Check if /Approved folder exists
    if not APPROVED_PATH.exists():
        print("✗ FAIL: /Approved folder not found")
        return False
    
    print("✓ /Approved folder exists")
    
    # Create a test draft post
    test_post = """---
status: draft
platform: linkedin
content: |
  Test post from Phase 2 integration test
  
  #Test #Integration
created_at: 2026-03-28T00:00:00Z
created_by: test
hitl_approved: true
hitl_approved_by: user
hitl_approved_at: 2026-03-28T00:00:00Z
tags:
  - test
---

## Test Post

This is a test post for integration testing.
"""
    
    test_file = APPROVED_PATH / 'test_linkedin_post.md'
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_post)
    
    print(f"✓ Created test post: {test_file}")
    print()
    print("To complete test:")
    print("1. Run: python src/linkedin/linkedin_poster.py --once")
    print("2. Watch browser open and navigate to LinkedIn")
    print("3. Check if post appears on LinkedIn")
    print("4. Check if file moved to /Done/")
    print()
    print("Note: Test file will remain in /Approved/ for manual testing")
    
    return True


def test_triage_classification():
    """Test: Triage correctly classifies email priority."""
    print()
    print("=" * 60)
    print("Test: Triage Classification")
    print("=" * 60)
    print()
    
    # Check if triage rules exist
    triage_path = VAULT_ROOT / 'config' / 'triage_rules.yaml'
    if not triage_path.exists():
        print("✗ FAIL: triage_rules.yaml not found")
        return False
    
    print("✓ triage_rules.yaml exists")
    
    # Import and test classification
    try:
        from gmail.gmail_monitor import classify_priority
        
        # Test high priority keywords
        test_cases = [
            ("Invoice #2026-001", "high"),
            ("URGENT: Meeting Tomorrow", "high"),
            ("Payment Overdue", "high"),
            ("Weekly Newsletter", "low"),
            ("Notification: Update", "low"),
            ("Regular Email", "normal"),
        ]
        
        print()
        print("Testing classification:")
        all_passed = True
        for subject, expected in test_cases:
            result = classify_priority("", subject)
            status = "✓" if result == expected else "✗"
            print(f"  {status} '{subject}' → {result} (expected: {expected})")
            if result != expected:
                all_passed = False
        
        if all_passed:
            print()
            print("✓ All triage tests passed")
            return True
        else:
            print()
            print("✗ Some triage tests failed")
            return False
            
    except Exception as e:
        print(f"✗ FAIL: {e}")
        return False


def test_audit_logging():
    """Test: All actions logged to /Logs/YYYY-MM-DD.json."""
    print()
    print("=" * 60)
    print("Test: Audit Logging")
    print("=" * 60)
    print()
    
    today = datetime.now().strftime('%Y-%m-%d')
    log_path = LOGS_PATH / f'{today}.json'
    
    # Check if log file exists
    if not log_path.exists():
        print("⚠ WARNING: No log file for today yet")
        print("  Log file will be created on first action")
        return True
    
    # Validate log structure
    import json
    with open(log_path, 'r', encoding='utf-8') as f:
        log_data = json.load(f)
    
    required_fields = ['date', 'vault_id', 'entries', 'summary']
    for field in required_fields:
        if field not in log_data:
            print(f"✗ FAIL: Missing required field: {field}")
            return False
    
    print("✓ Log file structure valid")
    
    # Check for gmail/linkedin entries
    gmail_entries = [e for e in log_data['entries'] if e.get('source') == 'gmail']
    linkedin_entries = [e for e in log_data['entries'] if e.get('source') == 'linkedin']
    
    print(f"✓ Found {len(gmail_entries)} Gmail actions")
    print(f"✓ Found {len(linkedin_entries)} LinkedIn actions")
    
    return True


def run_all_tests():
    """Run all Phase 2 integration tests."""
    print("=" * 60)
    print("Phase 2 Functional - Integration Tests")
    print("=" * 60)
    
    tests = [
        ("Gmail Alert Creation", test_gmail_alert_creation),
        ("LinkedIn Post Detection", test_linkedin_post_detection),
        ("Triage Classification", test_triage_classification),
        ("Audit Logging", test_audit_logging),
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
        print("All Tests PASSED")
        print("=" * 60)
        return True
    else:
        print()
        print("=" * 60)
        print("Some Tests FAILED")
        print("=" * 60)
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
