# Feature Specification: Dockerized Odoo AI Accountant

**Feature Branch**: `001-odoo-financial-sync`
**Created**: 2026-03-28
**Status**: Draft
**Phase**: Phase 4 of Digital Employee Vault - Integrating Automated Financial Tracking

## User Scenarios & Testing

### User Story 1 - Automated Marketing Expense Logging (Priority: P1)

As a business owner, I want every social media post to automatically create a marketing expense entry in Odoo, so that I don't have to manually track marketing costs.

**Why this priority**: This is the core value proposition - automatic financial tracking without manual intervention. Without this, there's no benefit to the integration.

**Independent Test**: After a successful social media post, verify an accounting entry appears in Odoo with the correct expense amount and description.

**Acceptance Scenarios**:

1. **Given** a social media post is successfully published, **When** the orchestrator completes, **Then** a marketing expense entry is created in Odoo with the base cost (500 PKR)
2. **Given** the Odoo container is unavailable, **When** a post is published, **Then** the system logs a warning but continues posting without crashing
3. **Given** multiple posts are published in sequence, **When** each completes, **Then** each creates a separate expense entry with timestamp

---

### User Story 2 - Secure Odoo Configuration Management (Priority: P2)

As a system administrator, I want to store Odoo credentials securely in environment variables, so that sensitive data is never exposed in code.

**Why this priority**: Security is critical for financial systems. Compromised credentials could lead to unauthorized financial data access.

**Independent Test**: Verify that no hardcoded credentials exist in source code and that the system reads from .env file successfully.

**Acceptance Scenarios**:

1. **Given** a .env file exists with ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASSWORD, **When** the system starts, **Then** it connects using these credentials
2. **Given** no .env file exists, **When** the system starts, **Then** it fails gracefully with a clear error message about missing configuration
3. **Given** credentials are in .env file, **When** code is reviewed, **Then** no hardcoded credentials are visible in source files

---

### User Story 3 - Docker Infrastructure Setup (Priority: P3)

As a DevOps engineer, I want Odoo and PostgreSQL running in Docker containers with persistent storage, so that the system is portable and data survives restarts.

**Why this priority**: Infrastructure enables the feature but doesn't deliver direct business value on its own. However, it's essential for production deployment.

**Independent Test**: Run docker-compose up and verify both Odoo (port 8069) and PostgreSQL containers start with data persistence.

**Acceptance Scenarios**:

1. **Given** docker-compose.yml is configured, **When** I run docker-compose up, **Then** Odoo runs on port 8069 and PostgreSQL runs on default port
2. **Given** containers are stopped and restarted, **When** they restart, **Then** all data persists (Odoo database and configurations remain intact)
3. **Given** volumes are mapped correctly, **When** container is removed and recreated, **Then** data remains accessible

---

### User Story 4 - Dynamic Cost Per Post (Priority: P4)

As a finance manager, I want to configure a base cost per social media post, so that marketing expenses are tracked consistently.

**Why this priority**: Allows business flexibility in cost tracking but is secondary to the core automation functionality.

**Independent Test**: Change the base cost configuration and verify new posts use the updated amount.

**Acceptance Scenarios**:

1. **Given** base cost is set to 500 PKR, **When** a post is published, **Then** the expense entry shows 500 PKR
2. **Given** base cost is changed to 750 PKR, **When** a new post is published, **Then** the expense entry shows 750 PKR
3. **Given** posts were made at different cost levels, **When** reviewing expense history, **Then** each entry shows the cost at time of posting

---

### Edge Cases

- What happens when Odoo container is down during posting? (System logs warning and continues)
- How does system handle Odoo API timeout? (Retry logic with exponential backoff, then log failure)
- What happens when Odoo credentials are invalid? (Clear error message, fail gracefully without stopping posts)
- How does system handle duplicate post logging? (Each post creates unique entry with timestamp)
- What happens when network connection is lost during Odoo call? (Log failure, continue with posting duties)

## Requirements

### Functional Requirements

- **FR-001**: System MUST create a marketing expense entry in Odoo after every successful social media post
- **FR-002**: System MUST read Odoo credentials (ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASSWORD) from environment variables or .env file
- **FR-003**: System MUST NEVER hardcode Odoo credentials in source code
- **FR-004**: System MUST log a "Financial Sync Failed" warning if Odoo is unavailable but continue posting
- **FR-005**: System MUST use a configurable base cost per post (default: 500 PKR)
- **FR-006**: System MUST authenticate with Odoo using XML-RPC protocol
- **FR-007**: System MUST create entries in Odoo's Account Move model for each expense
- **FR-008**: System MUST associate expenses with the correct account code (Marketing Expense, e.g., 500000)
- **FR-009**: System MUST include post timestamp and platform in the expense description
- **FR-010**: System MUST handle Odoo connection failures gracefully without crashing the posting workflow

### Key Entities

- **Social Media Post**: A published post on Facebook, Instagram, Twitter, or LinkedIn with timestamp, platform, and content
- **Marketing Expense**: An accounting entry in Odoo representing the cost of a social media post, linked to Marketing Expense account
- **Odoo Configuration**: Secure storage of Odoo connection details (URL, database, user, password)
- **Base Cost**: The standard cost per post in PKR that gets logged as an expense

## Success Criteria

1. **100% of successful social media posts** automatically create corresponding expense entries in Odoo (when Odoo is available)
2. **Zero hardcoded credentials** in source code - all credentials stored in .env file
3. **Zero posting interruptions** when Odoo is unavailable - system continues posting with logged warnings
4. **Expense entries created within 5 seconds** of post completion (when Odoo is responsive)
5. **System supports 100+ posts per day** without performance degradation
6. **Finance team can reconcile** marketing expenses by reviewing Odoo Account Move entries with post references

## Assumptions

- Odoo 17.0 is available and can be run via Docker
- PostgreSQL 15 is compatible with Odoo 17.0
- Social media posting workflow (Phase 3) is already functional
- Marketing Expense account (code 500000 or similar) exists in Odoo chart of accounts
- Base cost of 500 PKR is a reasonable default for social media posts
- XML-RPC is enabled on the Odoo instance
- Users have appropriate Odoo user permissions to create accounting entries

## Out of Scope

- Automatic invoice generation for marketing services
- Multi-currency support for international posting costs
- Integration with other Odoo modules (CRM, Sales, etc.)
- Real-time dashboard for marketing spend tracking
- Approval workflows for marketing expenses
- Bulk expense import/export functionality
- Custom Odoo module development (using standard Odoo features only)

## Dependencies

- **Phase 3 Social Media Suite**: Must be complete and functional (social_orchestrator.py)
- **Docker & Docker Compose**: Must be installed on deployment system
- **Odoo 17.0 Docker Image**: Must be available from official Odoo repository
- **PostgreSQL 15 Docker Image**: Must be available from official PostgreSQL repository
- **Python xmlrpc.client**: Standard library, no additional dependencies required
- **.env File Management**: python-dotenv or similar for loading environment variables

## Open Questions

None - all requirements are clear and can proceed to planning phase.
