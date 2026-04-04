# Odoo Docker Setup Guide

## Prerequisites

- Docker Desktop for Windows installed
- Docker Desktop running (check system tray for Docker icon)

## Quick Start

### 1. Start Docker Desktop

1. Open Docker Desktop from Start Menu
2. Wait for Docker to start (whale icon in system tray should be steady)
3. Verify Docker is running:
   ```bash
   docker info
   ```

### 2. Start Odoo Containers

From project root (`E:\hackathon_0_digital_fte\AI_Employee_vault`):

```bash
docker-compose up -d
```

### 3. Verify Containers Running

```bash
docker-compose ps
```

Expected output:
```
NAME          STATUS              PORTS
vault-db      Up (healthy)        5432/tcp
vault-odoo    Up (healthy)        0.0.0.0:8069->8069/tcp
```

### 4. Access Odoo

Open browser: `http://localhost:8069`

You should see the Odoo database creation screen.

### 5. Initialize Odoo Database

1. **Database Name**: `odoo_vault`
2. **Email**: your-email@example.com
3. **Password**: `admin`
4. Click **Create Database**

### 6. Install Invoicing Module

1. After login, click **Apps** in top menu
2. Search for "Invoicing"
3. Click **Install** on "Invoicing" app
4. Wait for installation to complete (~30 seconds)

### 7. Verify Chart of Accounts

1. Go to **Invoicing** → **Configuration** → **Chart of Accounts**
2. Look for account code `500000` (Marketing Expense)
3. If not found, create it:
   - Click **New**
   - **Code**: `500000`
   - **Name**: `Marketing Expense`
   - **Type**: `Expense`
   - Click **Save**

## Troubleshooting

### Docker Desktop Not Starting

**Error**: `open //./pipe/dockerDesktopLinuxEngine: The system cannot find the file specified`

**Solution**:
1. Start Docker Desktop manually from Start Menu
2. Wait for whale icon to appear in system tray
3. If it hangs, restart Docker Desktop:
   - Right-click tray icon → Quit Docker Desktop
   - Start Docker Desktop again

### Containers Not Starting

**Check logs**:
```bash
docker-compose logs
```

**Restart containers**:
```bash
docker-compose down
docker-compose up -d
```

### Cannot Access http://localhost:8069

**Check if port 8069 is in use**:
```bash
netstat -ano | findstr :8069
```

**Solution**: Change port in docker-compose.yml:
```yaml
ports:
  - "8070:8069"  # Use 8070 instead
```

Then update `.env`:
```
ODOO_URL=http://localhost:8070
```

## Stop Containers

```bash
docker-compose down
```

## Restart Containers

```bash
docker-compose restart
```

## View Logs

```bash
# All logs
docker-compose logs -f

# Odoo logs only
docker-compose logs -f web

# Database logs only
docker-compose logs -f db
```

## Next Steps

After completing setup:
1. ✅ Docker containers running
2. ✅ Database created (`odoo_vault`)
3. ✅ Invoicing module installed
4. ✅ Chart of Accounts configured
5. → Proceed to create `src/skills/odoo_manager.py`
