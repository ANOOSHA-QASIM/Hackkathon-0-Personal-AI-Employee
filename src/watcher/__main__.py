"""
Entry point for running the Digital FTE FileSystem Watcher.

Usage:
    python -m watcher
    python src/watcher/__main__.py
"""

from .file_watcher import run_watcher

if __name__ == '__main__':
    print("=" * 60)
    print("Digital FTE - FileSystem Watcher")
    print("=" * 60)
    print()
    print("Monitoring /Inbox for new files...")
    print("Press Ctrl+C to stop")
    print()
    run_watcher()
