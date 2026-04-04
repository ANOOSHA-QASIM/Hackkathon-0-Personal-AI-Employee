"""
Configuration settings for Digital FTE Vault - Phase 2.
Extends Phase 1 settings with Gmail/LinkedIn configuration.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Vault configuration (from Phase 1)
VAULT_ROOT = Path(os.environ.get('VAULT_ROOT', 'E:/hackathon_0_digital_fte/AI_Employee_vault'))

# Directory paths (from Phase 1)
INBOX_PATH = VAULT_ROOT / 'Inbox'
NEEDS_ACTION_PATH = VAULT_ROOT / 'Needs_Action'
IN_PROGRESS_PATH = VAULT_ROOT / 'In_Progress'
APPROVED_PATH = VAULT_ROOT / 'Approved'
REJECTED_PATH = VAULT_ROOT / 'Rejected'
DONE_PATH = VAULT_ROOT / 'Done'
LOGS_PATH = VAULT_ROOT / 'Logs'
ACCOUNTING_PATH = VAULT_ROOT / 'Accounting'
BRIEFINGS_PATH = VAULT_ROOT / 'Briefings'

# Phase 2: Gmail Configuration
GMAIL_POLL_INTERVAL = int(os.environ.get('GMAIL_POLL_INTERVAL', '300'))  # 5 minutes
GMAIL_MAX_RESULTS = int(os.environ.get('GMAIL_MAX_RESULTS', '5'))

# Phase 2: LinkedIn Configuration
LINKEDIN_POLL_INTERVAL = int(os.environ.get('LINKEDIN_POLL_INTERVAL', '120'))  # 2 minutes
LINKEDIN_EMAIL = os.environ.get('LINKEDIN_EMAIL', '')
LINKEDIN_PASSWORD = os.environ.get('LINKEDIN_PASSWORD', '')

# Phase 2: Triage Configuration
TRIAGE_RULES_PATH = VAULT_ROOT / 'config' / 'triage_rules.yaml'

# Credential paths
CREDENTIALS_PATH = VAULT_ROOT / 'credentials.json'
PROCESSED_EMAILS_PATH = LOGS_PATH / 'processed_emails.json'

# Watcher configuration (from Phase 1)
WATCHER_POLL_INTERVAL = int(os.environ.get('WATCHER_POLL_INTERVAL', '60'))
WATCHER_BATCH_SIZE = int(os.environ.get('WATCHER_BATCH_SIZE', '10'))

# Phase configuration
CURRENT_PHASE = int(os.environ.get('CURRENT_PHASE', '2'))


def ensure_directories():
    """Create all vault directories if they don't exist."""
    for path in [INBOX_PATH, NEEDS_ACTION_PATH, IN_PROGRESS_PATH, 
                 APPROVED_PATH, REJECTED_PATH, DONE_PATH, 
                 LOGS_PATH, ACCOUNTING_PATH, BRIEFINGS_PATH]:
        path.mkdir(parents=True, exist_ok=True)
    
    # Create config directory for triage rules
    (VAULT_ROOT / 'config').mkdir(parents=True, exist_ok=True)
