"""
CEO Briefer - Generates daily CEO briefing report from Odoo data.

Usage:
    python src/skills/ceo_briefer.py

Features:
    - Fetches today's journal entries from Odoo
    - Filters for Marketing Expense (Account 500000)
    - Calculates total posts and budget spent
    - Generates CEO_Report.md in vault root
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.skills.odoo_manager import OdooManager

# Vault root for report output
VAULT_ROOT = Path(os.environ.get(
    'VAULT_ROOT',
    'E:/hackathon_0_digital_fte/AI_Employee_vault'
))


class CEOBriefer:
    """Generates CEO briefing reports from Odoo data."""

    def __init__(self):
        """Initialize with Odoo connection."""
        self.odoo = OdooManager()
        self.report_path = VAULT_ROOT / 'CEO_Report.md'

    def fetch_today_entries(self) -> List[Dict[str, Any]]:
        """
        Fetch all journal entries for today from Odoo.

        Returns:
            List of journal entry dictionaries
        """
        if not self.odoo.check_connection():
            print("[CEO Briefer] ERROR: Cannot connect to Odoo")
            return []

        try:
            # Get today's date in Odoo format
            today = datetime.now().strftime('%Y-%m-%d')

            # Search for journal entries created today
            # Filter by date and move_type='entry' (journal entries)
            entry_ids = self.odoo.objects.execute_kw(
                self.odoo.db,
                self.odoo.uid,
                self.odoo.password,
                'account.move',
                'search',
                [[
                    ['date', '=', today],
                    ['move_type', '=', 'entry'],
                    ['state', 'in', ['posted', 'draft']]
                ]],
                {}
            )

            if not entry_ids:
                print(f"[CEO Briefer] No journal entries found for {today}")
                return []

            # Read entry details
            entries = self.odoo.objects.execute_kw(
                self.odoo.db,
                self.odoo.uid,
                self.odoo.password,
                'account.move',
                'read',
                [entry_ids],
                {
                    'fields': [
                        'name', 'date', 'ref', 'state',
                        'amount_total', 'line_ids'
                    ]
                }
            )

            print(f"[CEO Briefer] Found {len(entries)} journal entries for {today}")
            return entries

        except Exception as e:
            print(f"[CEO Briefer] Error fetching entries: {e}")
            return []

    def filter_marketing_expenses(self, entries: List[Dict]) -> List[Dict]:
        """
        Filter entries for Marketing Expense (Account 500000).

        Args:
            entries: List of journal entries

        Returns:
            Filtered list of marketing expense entries
        """
        marketing_entries = []

        for entry in entries:
            try:
                # Get line details
                line_ids = entry.get('line_ids', [])
                if not line_ids:
                    continue

                # Read line details
                lines = self.odoo.objects.execute_kw(
                    self.odoo.db,
                    self.odoo.uid,
                    self.odoo.password,
                    'account.move.line',
                    'read',
                    [line_ids],
                    {
                        'fields': [
                            'account_id', 'debit', 'credit', 'name'
                        ]
                    }
                )

                # Check if any line uses Marketing Expense account (500000)
                is_marketing = False
                amount = 0.0

                for line in lines:
                    account_id = line.get('account_id')
                    if account_id and isinstance(account_id, list):
                        account_code = account_id[0]  # Account ID
                        # Check account code
                        account_info = self.odoo.objects.execute_kw(
                            self.odoo.db,
                            self.odoo.uid,
                            self.odoo.password,
                            'account.account',
                            'read',
                            [[account_code]],
                            {'fields': ['code']}
                        )

                        if account_info and account_info[0].get('code') == '500000':
                            is_marketing = True
                            amount = line.get('debit', 0.0)
                            break

                if is_marketing:
                    marketing_entries.append({
                        'name': entry.get('name', ''),
                        'date': entry.get('date', ''),
                        'ref': entry.get('ref', ''),
                        'state': entry.get('state', ''),
                        'amount': amount
                    })

            except Exception as e:
                print(f"[CEO Briefer] Error processing entry {entry.get('name')}: {e}")
                continue

        print(f"[CEO Briefer] Found {len(marketing_entries)} marketing expense entries")
        return marketing_entries

    def calculate_totals(self, entries: List[Dict]) -> Dict[str, Any]:
        """
        Calculate total posts and budget spent.

        Args:
            entries: List of marketing expense entries

        Returns:
            Dictionary with totals
        """
        total_posts = len(entries)
        total_budget = sum(entry.get('amount', 0.0) for entry in entries)

        return {
            'total_posts': total_posts,
            'total_budget': total_budget,
            'currency': 'PKR'
        }

    def generate_report(self, entries: List[Dict], totals: Dict) -> str:
        """
        Generate CEO briefing report in Markdown format.

        Args:
            entries: List of marketing expense entries
            totals: Dictionary with totals

        Returns:
            Markdown report string
        """
        today = datetime.now().strftime('%Y-%m-%d')
        time_now = datetime.now().strftime('%H:%M:%S')

        # Build report
        report = f"""# CEO Daily Briefing Report

**Date**: {today}
**Generated**: {time_now}
**Source**: Odoo ERP - Marketing Expenses

---

## Executive Summary

| Metric | Value |
|--------|-------|
| **Total Posts Today** | {totals['total_posts']} |
| **Total Budget Spent** | {totals['total_budget']:,.2f} {totals['currency']} |
| **Average Cost Per Post** | {totals['total_budget'] / totals['total_posts']:,.2f} {totals['currency'] if totals['total_posts'] > 0 else 'N/A'} |

---

## Budget Analysis

"""

        if totals['total_posts'] > 0:
            report += f"✅ **Active**: {totals['total_posts']} post(s) published today\n"
            report += f"💰 **Spent**: {totals['total_budget']:,.2f} {totals['currency']}\n"
        else:
            report += "⚠️ **No Activity**: No marketing expenses recorded today\n"

        report += """
---

## Last 5 Activities

"""

        # Show last 5 entries
        last_5 = entries[-5:] if len(entries) > 5 else entries

        if last_5:
            report += "| # | Reference | Amount | Status |\n"
            report += "|---|-----------|--------|--------|\n"

            for i, entry in enumerate(reversed(last_5), 1):
                ref = entry.get('ref', 'N/A')
                amount = entry.get('amount', 0.0)
                state = entry.get('state', 'draft')
                status = '✅ Posted' if state == 'posted' else '📝 Draft'

                report += f"| {i} | {ref} | {amount:,.2f} {totals['currency']} | {status} |\n"
        else:
            report += "*No activities recorded today*\n"

        report += f"""
---

## Platform Breakdown

"""

        # Group by platform (extract from ref)
        platforms = {}
        for entry in entries:
            ref = entry.get('ref', '')
            # Extract platform from reference (e.g., "Social Post: facebook")
            if 'facebook' in ref.lower():
                platform = 'Facebook'
            elif 'twitter' in ref.lower():
                platform = 'Twitter'
            elif 'linkedin' in ref.lower():
                platform = 'LinkedIn'
            elif 'instagram' in ref.lower():
                platform = 'Instagram'
            else:
                platform = 'Other'

            if platform not in platforms:
                platforms[platform] = {'count': 0, 'amount': 0.0}

            platforms[platform]['count'] += 1
            platforms[platform]['amount'] += entry.get('amount', 0.0)

        if platforms:
            report += "| Platform | Posts | Amount |\n"
            report += "|----------|-------|--------|\n"

            for platform, data in sorted(platforms.items()):
                report += f"| {platform} | {data['count']} | {data['amount']:,.2f} {totals['currency']} |\n"
        else:
            report += "*No platform data available*\n"

        report += f"""
---

## Recommendations

"""

        if totals['total_posts'] == 0:
            report += "- ⚠️ No posts published today. Consider scheduling content.\n"
        elif totals['total_budget'] > 2000:
            report += "- 💰 High spending detected. Review budget allocation.\n"
        else:
            report += "- ✅ Spending within normal range.\n"
            report += "- 📊 Consider increasing post frequency for better engagement.\n"

        report += f"""
---

*Report generated automatically by AI Employee Vault*
*Next report: Tomorrow at 00:00*
"""

        return report

    def save_report(self, report: str):
        """
        Save report to vault root.

        Args:
            report: Markdown report string
        """
        try:
            with open(self.report_path, 'w', encoding='utf-8') as f:
                f.write(report)

            print(f"[CEO Briefer] Report saved to: {self.report_path}")
        except Exception as e:
            print(f"[CEO Briefer] Error saving report: {e}")
            raise

    def run(self):
        """Run the full CEO briefer workflow."""
        print("=" * 60)
        print("CEO Daily Briefing Report Generator")
        print("=" * 60)
        print()

        # Step 1: Connect to Odoo
        print("[Step 1] Connecting to Odoo...")
        if not self.odoo.authenticate():
            print("[CEO Briefer] ERROR: Cannot connect to Odoo")
            print("  Please ensure:")
            print("  1. Docker containers running: docker-compose ps")
            print("  2. Odoo accessible at http://localhost:8069")
            print("  3. Database 'odoo_vault' created")
            return False

        print(f"✓ Connected - UID: {self.odoo.uid}")

        # Step 2: Fetch today's entries
        print()
        print("[Step 2] Fetching today's journal entries...")
        entries = self.fetch_today_entries()

        # Step 3: Filter marketing expenses
        print()
        print("[Step 3] Filtering marketing expenses...")
        marketing_entries = self.filter_marketing_expenses(entries)

        # Step 4: Calculate totals
        print()
        print("[Step 4] Calculating totals...")
        totals = self.calculate_totals(marketing_entries)
        print(f"✓ Total Posts: {totals['total_posts']}")
        print(f"✓ Total Budget: {totals['total_budget']:,.2f} PKR")

        # Step 5: Generate report
        print()
        print("[Step 5] Generating CEO report...")
        report = self.generate_report(marketing_entries, totals)

        # Step 6: Save report
        print()
        print("[Step 6] Saving report...")
        self.save_report(report)

        print()
        print("=" * 60)
        print("✅ CEO BRIEFING REPORT COMPLETE")
        print("=" * 60)
        print(f"Report saved to: {self.report_path}")
        print()
        print("Next Steps:")
        print("  1. Open in Obsidian: CEO_Report.md")
        print("  2. Review daily metrics")
        print("  3. Check platform breakdown")
        print()

        return True


# Main execution
if __name__ == '__main__':
    briefer = CEOBriefer()
    success = briefer.run()
    sys.exit(0 if success else 1)
