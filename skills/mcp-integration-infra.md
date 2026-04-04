# MCP Integration Infrastructure Skill

## Purpose
Infrastructure skill for configuring Model Context Protocol (MCP) servers. Manages `mcp.json` for email-mcp, browser-mcp, and Odoo JSON-RPC integrations, ensuring secure credential handling via environment variables.

## Capabilities

### MCP Server Configuration
- Create and maintain `mcp.json` in project root
- Configure multiple MCP servers:
  - **email-mcp**: Gmail/Outlook integration
  - **browser-mcp**: Playwright-based browser automation
  - **odoo-mcp**: Odoo ERP JSON-RPC connector
  - **filesystem-mcp**: Enhanced file operations
- Manage server lifecycle (start, stop, restart)

### mcp.json Structure
```json
{
  "mcpServers": {
    "email-mcp": {
      "command": "node",
      "args": ["/path/to/email-mcp/dist/index.js"],
      "env": {
        "EMAIL_PROVIDER": "${EMAIL_PROVIDER}",
        "GMAIL_ACCESS_TOKEN": "${GMAIL_ACCESS_TOKEN}",
        "GMAIL_REFRESH_TOKEN": "${GMAIL_REFRESH_TOKEN}"
      }
    },
    "browser-mcp": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-playwright"],
      "env": {
        "BROWSER_PATH": "${BROWSER_PATH}",
        "HEADLESS": "false"
      }
    },
    "odoo-mcp": {
      "command": "python",
      "args": ["-m", "odoo_mcp"],
      "env": {
        "ODOO_URL": "${ODOO_URL}",
        "ODOO_DB": "${ODOO_DB}",
        "ODOO_USERNAME": "${ODOO_USERNAME}",
        "ODOO_API_KEY": "${ODOO_API_KEY}"
      }
    }
  }
}
```

### Environment Variable Management
- Create `.env.example` with placeholder values
- Validate `.env` exists before MCP startup
- Never log or expose sensitive values
- Support environment-specific configs (`.env.dev`, `.env.prod`)

### .env.example Template
```bash
# Email MCP
EMAIL_PROVIDER=gmail
GMAIL_ACCESS_TOKEN=your_access_token
GMAIL_REFRESH_TOKEN=your_refresh_token
GMAIL_CLIENT_ID=your_client_id
GMAIL_CLIENT_SECRET=your_client_secret

# Browser MCP
BROWSER_PATH=/usr/bin/google-chrome
HEADLESS=false

# Odoo MCP
ODOO_URL=https://your-instance.odoo.com
ODOO_DB=your_database
ODOO_USERNAME=your_username
ODOO_API_KEY=your_api_key

# Sync Infrastructure
SYNC_PROVIDER=git
CLOUD_VM_SSH_KEY=~/.ssh/cloud_vm
```

### Server Health Checks
```python
def check_mcp_servers() -> Dict[str, bool]:
    """Verify all MCP servers are responsive."""
    servers = load_mcp_config()
    health = {}
    for name, config in servers['mcpServers'].items():
        try:
            # Send ping via MCP protocol
            response = mcp_client.ping(name, timeout=5)
            health[name] = response.success
        except Exception as e:
            health[name] = False
            log_error(f"MCP server {name} health check failed: {e}")
    return health
```

### Credential Rotation
- Support token refresh workflows (OAuth2)
- Validate credentials on startup
- Notify on credential expiry
- Secure credential storage (OS keychain integration optional)

### Error Handling
- Missing env vars: Fail fast with clear error message
- Server startup failure: Log stderr, retry with backoff
- Connection timeout: Exponential backoff, circuit breaker
- Invalid config: Validate schema before applying

### Security Best Practices
- Use app-specific credentials where possible
- Rotate API keys periodically
- Limit MCP server permissions (least privilege)
- Audit MCP server access logs
- Encrypt sensitive data at rest

### Integration with Sentinel Scripts
```python
# Sentinel script uses MCP servers
from mcp_client import MCPClient

client = MCPClient()
await client.connect('email-mcp')

# Check for new emails
emails = await client.call('email-mcp', 'list_unread', {
    'label': 'INBOX',
    'since': last_check.isoformat()
})

# Transform to vault tasks
for email in emails:
    create_vault_task(transform_email(email))
```

### Troubleshooting
- Check `mcp.json` syntax (JSON validation)
- Verify env vars are loaded (`printenv | grep MCP`)
- Test server connectivity manually
- Review MCP server logs (`~/.mcp/logs/`)
- Validate network/firewall rules
