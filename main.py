"""
Unified Master Orchestrator - Continuous Automation Loop

Sequences all AI Employee workflows in a continuous loop:
1. Gmail Monitor - Fetch new emails → /Needs_Action
2. Auto-Drafter - Generate AI replies → /In_Progress
3. Social Orchestrator - Post approved content → Odoo logging
4. Gmail Sender - Send approved replies → Gmail
5. CEO Briefer - Update daily report → CEO_Report.md

Usage:
    python main.py

Features:
    - Continuous loop with 5-minute delay
    - Error isolation (one failure doesn't stop others)
    - Automatic CEO report updates
    - Graceful shutdown (Ctrl+C)
"""

import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

# Vault root
VAULT_ROOT = Path(__file__).parent

# Script paths
SCRIPTS = {
    'gmail_monitor': VAULT_ROOT / 'src' / 'gmail' / 'gmail_monitor.py',
    'auto_drafter': VAULT_ROOT / 'src' / 'agent' / 'auto_drafter.py',
    'social_orchestrator': VAULT_ROOT / 'src' / 'skills' / 'social_orchestrator.py',
    'gmail_sender': VAULT_ROOT / 'src' / 'gmail' / 'gmail_sender.py',
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
        'gmail_monitor': False,
        'auto_drafter': False,
        'social_orchestrator': False,
        'gmail_sender': False,
        'ceo_briefer': False
    }

    print()
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "AI EMPLOYEE - AUTOMATION CYCLE" + " " * 17 + "║")
    print("║" + f"  Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}" + " " * 26 + "║")
    print("╚" + "=" * 58 + "╝")

    # Step 1: Gmail Monitor
    try:
        results['gmail_monitor'] = run_script(
            'Gmail Monitor',
            SCRIPTS['gmail_monitor']
        )
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"[Gmail Monitor] ✗ Error: {e}")

    # Step 2: Auto-Drafter
    try:
        results['auto_drafter'] = run_script(
            'Auto-Drafter',
            SCRIPTS['auto_drafter']
        )
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"[Auto-Drafter] ✗ Error: {e}")

    # Step 3: Social Orchestrator
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

    # Step 4: Gmail Sender
    try:
        results['gmail_sender'] = run_script(
            'Gmail Sender',
            SCRIPTS['gmail_sender']
        )
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"[Gmail Sender] ✗ Error: {e}")

    # Step 5: CEO Briefer (only if any step succeeded)
    if any([results['gmail_monitor'], results['auto_drafter'],
            results['social_orchestrator'], results['gmail_sender']]):
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
    print("AI Employee - Unified Master Orchestrator")
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
