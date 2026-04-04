"""
LinkedIn Module Entry Point

Usage:
    python -m linkedin  # Run poster continuously
    python -m linkedin --once  # Run once
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from linkedin import linkedin_poster, post_scheduler


def main():
    """Main entry point for linkedin module."""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--once':
            linkedin_poster.check_approved_posts()
        elif sys.argv[1] == '--schedule':
            post_scheduler.run_scheduler()
        else:
            linkedin_poster.run_poster()
    else:
        # Default: run poster continuously
        linkedin_poster.run_poster()


if __name__ == '__main__':
    main()
