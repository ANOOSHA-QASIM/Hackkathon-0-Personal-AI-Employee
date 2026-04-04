# Odoo Account Setup Guide

## Current Status

✅ Docker containers running
✅ Odoo accessible at http://localhost:8069
✅ Database created: `odoo_vault`
✅ Python connection working (UID: 2)
⚠️ Marketing Expense account needs to be created

---

## Create Marketing Expense Account

### Option 1: Via Odoo UI (Recommended)

1. **Open Odoo**: http://localhost:8069
2. **Login** with admin credentials
3. **Go to**: Invoicing → Configuration → Chart of Accounts
4. **Click**: "New" button
5. **Fill in**:
   - **Code**: `500000`
   - **Name**: `Marketing Expense`
   - **Type**: `Expense`
   - **Allowed to Reconcile**: No
6. **Click**: "Save"

### Option 2: Via Python Script

Run this script to create the account automatically:

```python
# create_marketing_account.py
import xmlrpc.client

url = 'http://localhost:8069'
db = 'odoo_vault'
username = 'admin'
password = 'admin'

# Authenticate
common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
uid = common.authenticate(db, username, password, {})

if uid:
    objects = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
    
    # Create account
    account_id = objects.execute_kw(
        db, uid, password,
        'account.account',
        'create',
        [{
            'code': '500000',
            'name': 'Marketing Expense',
            'user_type_id': objects.execute_kw(
                db, uid, password,
                'account.account.type',
                'search',
                [[('type', '=', 'other')]],
                {'limit': 1}
            )[0],
            'reconcile': False
        }]
    )
    print(f"Account created with ID: {account_id}")
else:
    print("Authentication failed")
```

---

## Verify Account Created

### In Odoo UI:

1. Go to: Invoicing → Configuration → Chart of Accounts
2. Search for: `500000`
3. Should see: "Marketing Expense"

### Via Python:

```bash
python src/skills/odoo_manager.py
```

Should show:
```
[Test] Testing journal entry creation...
[Odoo] Journal entry created - Move ID: 123
✓ Test journal entry created - Move ID: 123
```

---

## Next Steps After Account Setup

1. ✅ Create Marketing Expense account (500000)
2. → Run test script again: `python src/skills/odoo_manager.py`
3. → Verify journal entry appears in Odoo: Invoicing → Accounting → Journal Entries
4. → Proceed to integrate with social orchestrator

---

## Troubleshooting

### Account Type Not Found

If you get an error about account type, manually select:
- **Account Type**: Expense (or "Other" if Expense not available)

### Invoicing Module Not Installed

If you don't see "Invoicing" in the dashboard:
1. Go to: Apps
2. Search: "Invoicing"
3. Click: "Install"
4. Wait for installation to complete

### Cannot Access Odoo

If http://localhost:8069 doesn't work:
```bash
docker-compose ps
docker-compose logs web
```
