# Automated Accounting (Odoo) Skill

## Purpose
Implementation skill for financial automation. Audits `Bank_Transactions.md` and interfaces with Odoo Community 19+ via JSON-RPC for invoice generation, payment tracking, and weekly revenue reporting.

## Capabilities

### Bank Transaction Auditing
- Parse `Bank_Transactions.md` with structured format:
```markdown
---
period: 2026-W13
source: bank_export_csv
last_sync: 2026-03-28T09:00:00Z
---

## Transactions

| Date | Description | Amount | Currency | Counterparty | Status |
|------|-------------|--------|----------|--------------|--------|
| 2026-03-27 | Invoice Payment | 1500.00 | USD | Acme Corp | reconciled |
| 2026-03-27 | Office Supplies | -45.99 | USD | Staples | pending |
| 2026-03-26 | Client Payment | 2300.00 | USD | TechStart Inc | reconciled |
```
- Validate transaction integrity:
  - Duplicate detection (same date, amount, counterparty)
  - Missing counterparty identification
  - Unusual amounts (threshold alerts)
  - Currency conversion accuracy
- Flag anomalies for human review → move to `/Needs_Action/`

### Odoo JSON-RPC Integration
```python
import requests
from typing import Dict, Any, List

class OdooClient:
    def __init__(self, url: str, db: str, username: str, api_key: str):
        self.url = f"{url}/jsonrpc"
        self.db = db
        self.username = username
        self.api_key = api_key
        self.uid = self._authenticate()
    
    def _authenticate(self) -> int:
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "common",
                "method": "authenticate",
                "args": [self.db, self.username, self.api_key, {}]
            },
            "id": 1
        }
        response = requests.post(self.url, json=payload)
        return response.json()['result']
    
    def create_invoice(self, invoice_data: Dict) -> int:
        """Create invoice in Odoo, return invoice ID."""
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db, self.uid, self.api_key,
                    "account.move",
                    "create",
                    [{
                        "move_type": "out_invoice",
                        "partner_id": invoice_data['partner_id'],
                        "invoice_date": invoice_data['date'],
                        "invoice_line_ids": invoice_data['lines'],
                        "ref": invoice_data.get('reference', '')
                    }]
                ]
            },
            "id": 2
        }
        response = requests.post(self.url, json=payload)
        return response.json()['result']
    
    def get_unpaid_invoices(self, partner_id: int = None) -> List[Dict]:
        """Fetch unpaid invoices, optionally filtered by partner."""
        domain = [["payment_state", "=", "not_paid"]]
        if partner_id:
            domain.append(["partner_id", "=", partner_id])
        
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "service": "object",
                "method": "execute_kw",
                "args": [
                    self.db, self.uid, self.api_key,
                    "account.move",
                    "search_read",
                    [domain],
                    {"fields": ["id", "name", "amount_total", "date", "partner_id"]}
                ]
            },
            "id": 3
        }
        response = requests.post(self.url, json=payload)
        return response.json()['result']
```

### Invoice Generation Workflow
1. Extract transaction from `Bank_Transactions.md`
2. Match counterparty to Odoo partner (by name/email)
3. Create partner if not exists (with human approval)
4. Generate invoice line items from transaction details
5. Post invoice → move task to `/Approved/` for human review
6. On approval, send invoice via email-mcp

### Payment Tracking
- Monitor Odoo for payment state changes
- Reconcile payments with bank transactions
- Update `Bank_Transactions.md` with reconciliation status
- Flag partial payments or discrepancies

### Weekly Revenue Report
```python
def generate_weekly_revenue_report(week_number: int, year: int) -> Dict:
    """Generate revenue summary for given week."""
    client = OdooClient(ODOO_URL, ODOO_DB, ODOO_USER, ODOO_API_KEY)
    
    # Date range for week
    start_date, end_date = get_week_dates(week_number, year)
    
    # Fetch paid invoices in range
    domain = [
        ["payment_state", "=", "paid"],
        ["invoice_date", ">=", start_date],
        ["invoice_date", "<=", end_date]
    ]
    
    invoices = client.search_read(
        "account.move",
        domain,
        fields=["id", "name", "amount_total", "amount_untaxed", 
                "amount_tax", "partner_id", "invoice_date"]
    )
    
    # Aggregate by partner
    by_partner = {}
    total_revenue = 0
    for inv in invoices:
        partner = inv['partner_id'][1] if isinstance(inv['partner_id'], list) else "Unknown"
        if partner not in by_partner:
            by_partner[partner] = 0
        by_partner[partner] += inv['amount_total']
        total_revenue += inv['amount_total']
    
    return {
        "week": week_number,
        "year": year,
        "total_revenue": total_revenue,
        "invoice_count": len(invoices),
        "by_partner": by_partner,
        "top_clients": sorted(by_partner.items(), key=lambda x: x[1], reverse=True)[:5]
    }
```

### Report Output Format
```markdown
---
report_type: weekly_revenue
week: 13
year: 2026
generated_at: 2026-03-28T10:00:00Z
---

# Weekly Revenue Report - Week 13, 2026

## Summary
- **Total Revenue**: $15,450.00
- **Invoices Paid**: 12
- **Outstanding**: $3,200.00 (4 invoices)

## Top Clients
| Client | Revenue |
|--------|---------|
| Acme Corp | $5,500.00 |
| TechStart Inc | $4,300.00 |
| Global Services | $2,150.00 |

## Outstanding Invoices
| Invoice | Client | Amount | Due Date |
|---------|--------|--------|----------|
| INV/2026/0045 | Widget Co | $1,200.00 | 2026-04-05 |
| INV/2026/0048 | StartupXYZ | $2,000.00 | 2026-04-10 |
```

## Configuration
```yaml
odoo:
  url: "${ODOO_URL}"
  database: "${ODOO_DB}"
  username: "${ODOO_USERNAME}"
  api_key: "${ODOO_API_KEY}"
  
accounting:
  bank_transactions_file: "./Bank_Transactions.md"
  auto_reconcile: false  # Require HITL approval
  currency: USD
  tax_rate: 0.08
  
reporting:
  weekly_report_day: Friday
  weekly_report_hour: 17
  recipients: ["finance@company.com"]
```

## Error Handling
- Odoo connection failure: Retry with exponential backoff (max 3)
- Partner not found: Create draft partner, flag for human review
- Duplicate invoice detection: Warn and skip
- Amount mismatch: Log discrepancy, move to `/Needs_Action/`
- API rate limits: Respect Odoo rate limiting, queue requests

## Security
- API keys in `.env` only
- Audit log for all financial operations
- HITL required for: invoice creation, payment posting, refunds
- Daily JSON audit logs in `/audit/`
