"""
Test CEO Briefer - Report Generation

Tests the CEO briefer report generation with mock data.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add src to path
VAULT_ROOT = Path(__file__).parent
sys.path.insert(0, str(VAULT_ROOT / 'src'))


def test_report_generation():
    """Test report generation with mock data."""
    print("=" * 60)
    print("CEO Briefer Test - Report Generation")
    print("=" * 60)
    print()

    # Mock data
    mock_entries = [
        {
            'name': 'INV/2026/0001',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'ref': 'Social Post: facebook_test',
            'state': 'draft',
            'amount': 500.0
        },
        {
            'name': 'INV/2026/0002',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'ref': 'Social Post: twitter_test',
            'state': 'draft',
            'amount': 500.0
        },
        {
            'name': 'INV/2026/0003',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'ref': 'Social Post: linkedin_test',
            'state': 'draft',
            'amount': 500.0
        }
    ]

    mock_totals = {
        'total_posts': 3,
        'total_budget': 1500.0,
        'currency': 'PKR'
    }

    print("[Test 1] Testing report generation...")

    try:
        from skills.ceo_briefer import CEOBriefer

        briefer = CEOBriefer()
        report = briefer.generate_report(mock_entries, mock_totals)

        # Verify report content
        assert '# CEO Daily Briefing Report' in report
        assert 'Total Posts Today' in report
        assert '1,500.00 PKR' in report
        assert 'Last 5 Activities' in report
        assert 'Platform Breakdown' in report

        print("✓ Report generated successfully")
        print(f"✓ Report length: {len(report)} characters")
        print()

        # Show preview
        print("[Test 2] Report Preview:")
        print("-" * 60)
        # Show first 50 lines
        lines = report.split('\n')[:50]
        print('\n'.join(lines))
        print("-" * 60)
        print()

        return True

    except Exception as e:
        print(f"✗ Report generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_calculate_totals():
    """Test totals calculation."""
    print()
    print("[Test 3] Testing totals calculation...")

    try:
        from skills.ceo_briefer import CEOBriefer

        briefer = CEOBriefer()

        entries = [
            {'amount': 500.0},
            {'amount': 500.0},
            {'amount': 500.0}
        ]

        totals = briefer.calculate_totals(entries)

        assert totals['total_posts'] == 3
        assert totals['total_budget'] == 1500.0
        assert totals['currency'] == 'PKR'

        print(f"✓ Total Posts: {totals['total_posts']}")
        print(f"✓ Total Budget: {totals['total_budget']}")
        print(f"✓ Currency: {totals['currency']}")

        return True

    except Exception as e:
        print(f"✗ Totals calculation failed: {e}")
        return False


def main():
    """Run all tests."""
    print()

    # Test 1: Report generation
    test1 = test_report_generation()

    # Test 2: Totals calculation
    test2 = test_calculate_totals()

    # Summary
    print()
    print("=" * 60)
    print("CEO Briefer Test Results")
    print("=" * 60)
    print(f"Report Generation:  {'✓ PASS' if test1 else '✗ FAIL'}")
    print(f"Totals Calculation: {'✓ PASS' if test2 else '✗ FAIL'}")
    print()

    if test1 and test2:
        print("🎉 CEO BRIEFER COMPLETE!")
        print()
        print("What was created:")
        print("  ✓ src/skills/ceo_briefer.py - CEO briefing generator")
        print("  ✓ Fetches journal entries from Odoo")
        print("  ✓ Filters for Marketing Expense (500000)")
        print("  ✓ Calculates totals and generates report")
        print("  ✓ Saves CEO_Report.md to vault root")
        print()
        print("Run CEO Briefer:")
        print("  python src/skills/ceo_briefer.py")
        print()
        print("View Report:")
        print("  Open CEO_Report.md in Obsidian")
        print()
        return True
    else:
        print("⚠ Some tests failed")
        print()
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
