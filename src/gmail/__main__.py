"""
Gmail Module Entry Point

Usage:
    python -m gmail --authenticate
    python -m gmail --test
    python -m gmail  # Run monitor continuously
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from gmail import gmail_monitor, gmail_auth


def main():
    """Main entry point for gmail module."""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--authenticate':
            gmail_auth.main()
        elif sys.argv[1] == '--test':
            gmail_auth.test_gmail_connection()
        elif sys.argv[1] == '--once':
            gmail_monitor.check_unread_emails()
        else:
            gmail_monitor.run_monitor()
    else:
        # Default: run monitor continuously
        gmail_monitor.run_monitor()


if __name__ == '__main__':
    main()
