"""
Unified Master Orchestrator - Social Media & Odoo Automation

Continuous automation loop for social media posting and financial tracking:
1. Social Orchestrator - Post approved content → Odoo logging
2. CEO Briefer - Update daily report → CEO_Report.md

Usage:
    python main.py

Features:
    - Continuous loop with 5-minute delay
    - Error isolation (one failure doesn't stop others)
    - Automatic CEO report updates
    - Graceful shutdown (Ctrl+C)
    - Odoo expense logging for all platforms
"""

import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Vault root
VAULT_ROOT = Path(__file__).parent

# Script Paths (Social Media + Odoo only)
SCRIPTS = {
    'social_orchestrator': VAULT_ROOT / 'src' / 'skills' / 'social_orchestrator.py',
    'ceo_briefer': VAULT_ROOT / 'src' / 'skills' / 'ceo_briefer.py',
}

# Loop interval (5 minutes)
LOOP_INTERVAL = 300  # seconds


def run_script(name, script_path, args=None):
    """
    Run a Python script with error handling.

    Args:
        name: Script name for logging
        script_path: Path to script
        args: Optional list of arguments

    Returns:
        True if successful, False otherwise
    """
    if not script_path.exists():
        print(f"[{name}] ⚠ Script not found: {script_path}")
        return False

    print()
    print("=" * 60)
    print(f"[{name}] Starting...")
    print("=" * 60)

    try:
        # Build command
        cmd = [sys.executable, str(script_path)]
        if args:
            cmd.extend(args)

        # Run script
        result = subprocess.run(
            cmd,
            cwd=str(VAULT_ROOT),
            capture_output=False,  # Show output in real-time
            timeout=600  # 10 minute timeout per script
        )

        if result.returncode == 0:
            print(f"[{name}] ✓ Completed successfully")
            return True
        else:
            print(f"[{name}] ✗ Failed with exit code {result.returncode}")
            return False

    except subprocess.TimeoutExpired:
        print(f"[{name}] ⏱ Timeout after 10 minutes")
        return False
    except KeyboardInterrupt:
        print(f"\n[{name}] ⚠ Interrupted by user")
        raise
    except Exception as e:
        print(f"[{name}] ✗ Error: {e}")
        return False


def run_cycle():
    """
    Run one complete automation cycle.

    Returns:
        Dictionary with success status for each step
    """
    results = {
        'social_orchestrator': False,
        'ceo_briefer': False
    }

    print()
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 8 + "AI EMPLOYEE - SOCIAL MEDIA CYCLE" + " " * 16 + "║")
    print("║" + f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + " " * 26 + "║")
    print("╚" + "=" * 58 + "╝")

    # Step 1: Social Orchestrator (Posts to LinkedIn, Meta, Twitter + Odoo logging)
    try:
        results['social_orchestrator'] = run_script(
            'Social Orchestrator',
            SCRIPTS['social_orchestrator'],
            args=['--once']  # Run once, not continuous
        )
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"[Social Orchestrator] ✗ Error: {e}")

    # Step 2: CEO Briefer (Update report if social orchestrator succeeded)
    if results['social_orchestrator']:
        try:
            results['ceo_briefer'] = run_script(
                'CEO Briefer',
                SCRIPTS['ceo_briefer']
            )
        except KeyboardInterrupt:
            raise
        except Exception as e:
            print(f"[CEO Briefer] ✗ Error: {e}")

    return results


def print_cycle_summary(results):
    """Print summary of cycle results."""
    print()
    print("=" * 60)
    print("CYCLE SUMMARY")
    print("=" * 60)

    for name, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {name:25} {status}")

    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)

    print()
    print(f"Success: {success_count}/{total_count} steps completed")
    print("=" * 60)


def main():
    """Main continuous loop."""
    print("=" * 60)
    print("AI Employee - Social Media & Odoo Orchestrator")
    print("=" * 60)
    print()
    print("Starting continuous automation loop...")
    print(f"Cycle interval: {LOOP_INTERVAL // 60} minutes")
    print("Press Ctrl+C to stop")
    print()

    cycle_count = 0

    try:
        while True:
            cycle_count += 1

            # Run one cycle
            try:
                results = run_cycle()
                print_cycle_summary(results)
            except KeyboardInterrupt:
                print("\n⚠ Cycle interrupted")
                break
            except Exception as e:
                print(f"\n✗ Cycle error: {e}")

            # Wait for next cycle
            print()
            print(f"Waiting {LOOP_INTERVAL // 60} minutes for next cycle...")
            print(f"Next cycle: {(datetime.now().timestamp() + LOOP_INTERVAL):.0f}")
            print("(Press Ctrl+C to stop)")
            print()

            time.sleep(LOOP_INTERVAL)

    except KeyboardInterrupt:
        print()
        print("=" * 60)
        print("SHUTTING DOWN")
        print("=" * 60)
        print(f"Total cycles completed: {cycle_count}")
        print()
        print("Graceful shutdown complete")
        print("AI Employee is now sleeping... 💤")
        print()


if __name__ == '__main__':
    main()
