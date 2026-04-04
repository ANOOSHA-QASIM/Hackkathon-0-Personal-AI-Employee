"""
Agent Module Entry Point

Usage:
    python -m agent  # Run auto-drafter continuously
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agent.auto_drafter import run_drafter


def main():
    """Main entry point for agent module."""
    # Default: run auto-drafter continuously
    run_drafter()


if __name__ == '__main__':
    main()
