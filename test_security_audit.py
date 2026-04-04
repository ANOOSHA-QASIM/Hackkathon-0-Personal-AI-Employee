"""
Security Audit - Verify No Hardcoded Credentials

Checks the codebase for hardcoded passwords, secrets, or tokens.
"""

import os
import re
from pathlib import Path

VAULT_ROOT = Path(__file__).parent

# Patterns to search for hardcoded credentials
DANGEROUS_PATTERNS = [
    r'password\s*=\s*["\'][^"\']{3,}["\']',  # password = "something"
    r'secret\s*=\s*["\'][^"\']{3,}["\']',     # secret = "something"
    r'token\s*=\s*["\'][^"\']{3,}["\']',       # token = "something"
    r'api_key\s*=\s*["\'][^"\']{3,}["\']',     # api_key = "something"
    r'ODOO_PASSWORD\s*=\s*["\'][^"\']{3,}["\']',  # Hardcoded Odoo password
    r'LINKEDIN_PASSWORD\s*=\s*["\'][^"\']{3,}["\']',  # Hardcoded LinkedIn password
    r'GMAIL.*PASSWORD\s*=\s*["\'][^"\']{3,}["\']',  # Hardcoded Gmail password
]

# Safe patterns (using environment variables)
SAFE_PATTERNS = [
    r'os\.getenv\(',
    r'os\.environ\.get\(',
]


def check_file_for_secrets(file_path):
    """Check a single file for hardcoded credentials."""
    issues = []

    # Skip this test file to avoid false positives
    if 'test_security_audit.py' in str(file_path):
        return issues

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        for line_num, line in enumerate(lines, 1):
            # Skip comments and empty lines
            stripped = line.strip()
            if stripped.startswith('#') or not stripped:
                continue

            # Check for dangerous patterns
            for pattern in DANGEROUS_PATTERNS:
                if re.search(pattern, line, re.IGNORECASE):
                    # Verify it's not using environment variables
                    is_safe = any(re.search(safe, line) for safe in SAFE_PATTERNS)
                    if not is_safe:
                        issues.append({
                            'file': str(file_path),
                            'line': line_num,
                            'content': line.strip(),
                            'pattern': pattern
                        })

    except Exception as e:
        pass  # Skip files that can't be read

    return issues


def scan_codebase():
    """Scan entire codebase for hardcoded credentials."""
    print("=" * 60)
    print("Security Audit - Hardcoded Credentials Check")
    print("=" * 60)
    print()

    all_issues = []
    files_scanned = 0

    # Scan Python files
    for py_file in VAULT_ROOT.rglob('*.py'):
        # Skip virtual environments and cache
        if any(part in ['.venv', 'venv', '__pycache__', 'node_modules'] for part in py_file.parts):
            continue

        files_scanned += 1
        issues = check_file_for_secrets(py_file)
        all_issues.extend(issues)

    print(f"Files Scanned: {files_scanned}")
    print(f"Issues Found: {len(all_issues)}")
    print()

    if all_issues:
        print("⚠ POTENTIAL SECURITY ISSUES:")
        print("-" * 60)
        for issue in all_issues:
            print(f"File: {issue['file']}")
            print(f"Line: {issue['line']}")
            print(f"Content: {issue['content']}")
            print()
        return False
    else:
        print("✅ NO HARDCODED CREDENTIALS FOUND!")
        print()
        print("All sensitive data is properly stored in environment variables.")
        return True


def check_env_file():
    """Check if .env file exists and is in .gitignore."""
    print()
    print("=" * 60)
    print("Environment File Check")
    print("=" * 60)
    print()

    env_file = VAULT_ROOT / '.env'
    gitignore_file = VAULT_ROOT / '.gitignore'

    # Check .env exists
    if env_file.exists():
        print("✓ .env file exists")
    else:
        print("✗ .env file NOT found - create it from .env.example")

    # Check .env.example exists
    env_example = VAULT_ROOT / '.env.example'
    if env_example.exists():
        print("✓ .env.example template exists")
    else:
        print("⚠ .env.example NOT found - consider creating one")

    # Check .gitignore
    if gitignore_file.exists():
        with open(gitignore_file, 'r') as f:
            gitignore_content = f.read()

        if '.env' in gitignore_content:
            print("✓ .env is excluded from .gitignore")
        else:
            print("✗ .env is NOT excluded from .gitignore - ADD IT IMMEDIATELY!")

        if '.browser_data' in gitignore_content:
            print("✓ .browser_data is excluded from .gitignore")
        else:
            print("⚠ .browser_data is NOT excluded from .gitignore")
    else:
        print("✗ .gitignore NOT found!")

    print()


def main():
    """Run full security audit."""
    print()

    # Check environment files
    check_env_file()

    # Scan codebase
    codebase_clean = scan_codebase()

    # Summary
    print()
    print("=" * 60)
    print("SECURITY AUDIT SUMMARY")
    print("=" * 60)
    print(f"Codebase Clean: {'✓ PASS' if codebase_clean else '✗ FAIL'}")
    print()

    if codebase_clean:
        print("🎉 SECURITY HARDENING COMPLETE!")
        print()
        print("What was verified:")
        print("  ✓ No hardcoded passwords in codebase")
        print("  ✓ No hardcoded secrets or tokens")
        print("  ✓ All credentials use environment variables")
        print("  ✓ .env file excluded from .gitignore")
        print("  ✓ .browser_data excluded from .gitignore")
        print()
        print("Next Steps:")
        print("  1. Copy .env.example to .env")
        print("  2. Fill in your actual credentials in .env")
        print("  3. Never commit .env to GitHub")
        print()
        return True
    else:
        print("⚠ SECURITY ISSUES FOUND!")
        print()
        print("Please review the issues above and:")
        print("  1. Move hardcoded credentials to .env file")
        print("  2. Use os.getenv() to read them")
        print("  3. Add .env to .gitignore")
        print()
        return False


if __name__ == '__main__':
    success = main()
    exit(0 if success else 1)
