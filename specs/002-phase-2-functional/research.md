# Technical Research: Phase 2 Functional

**Feature**: 002-phase-2-functional  
**Date**: 2026-03-28  
**Status**: Complete

## Research Summary

This document resolves all technical unknowns for Phase 2 Functional (Gmail monitoring, LinkedIn posting, communication triage). Each section includes the decision made, rationale, and alternatives considered.

---

## 1. Gmail API Integration Pattern

**Question**: What is the best approach for monitoring Gmail for unread emails?

### Decision
Use **`google-api-python-client`** with OAuth2 credentials (credentials.json) for Gmail API access.

### Rationale
- **Official library**: Google-maintained, well-documented, stable API
- **OAuth2 support**: Secure authentication flow, token refresh
- **Unread filtering**: Native support for querying unread emails only
- **Message metadata**: Access to headers (sender, subject, date) without downloading full body
- **Quota management**: Gmail API quota sufficient for 5-minute polling

### Implementation Pattern
```python
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Load credentials from credentials.json
creds = Credentials.from_authorized_user_file('credentials.json')
service = build('gmail', 'v1', credentials=creds)

# Query unread emails
results = service.users().messages().list(
    userId='me',
    q='is:unread',
    maxResults=10
).execute()
```

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| IMAP (imaplib) | Built-in Python, no dependencies | Deprecated by Google, 2FA issues, less secure | Google discourages IMAP for new apps |
| Gmail MCP Server | Pre-built integration | Additional infrastructure, complexity | Direct API simpler for Phase 2 |
| google-auth-library | More control over auth | Lower-level, more code needed | google-api-python-client is higher-level |

---

## 2. LinkedIn Posting Method

**Question**: What is the best approach for posting to LinkedIn?

### Decision
Use **Playwright** for browser automation (not LinkedIn API).

### Rationale
- **No API approval required**: LinkedIn API requires business verification (weeks of delay)
- **Full functionality**: Browser automation supports all post types (text, images, articles)
- **No API limits**: LinkedIn API has strict rate limits; Playwright limited only by browser
- **Consistent with Phase 1**: Playwright MCP already available from Phase 1 infrastructure

### Implementation Pattern
```python
from playwright.async_api import async_playwright

async def post_to_linkedin(content: str, image_path: str = None):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto('https://www.linkedin.com/feed/')
        
        # Click share box
        await page.click('.share-box-feed-entry__trigger')
        
        # Type content
        await page.fill('.ql-editor', content)
        
        # Upload image if provided
        if image_path:
            async with page.expect_file_chooser() as fc_info:
                await page.click('button[aria-label="Media"]')
            chooser = await fc_info.value
            await chooser.set_files(image_path)
        
        # Click post
        await page.click('button:has-text("Post")')
```

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| LinkedIn API | Official, stable | Business verification required (2-4 weeks), limited post types | Too slow for Phase 2 timeline |
| Third-party services (Buffer, Hootsuite) | Easy integration | Monthly cost, security concerns (store credentials externally) | Violates Phase 1 security principles |
| Requests + LinkedIn API | Direct HTTP calls | Complex OAuth flow, rate limits, limited functionality | Playwright provides better UX |

---

## 3. Priority Classification Logic

**Question**: How should emails and messages be categorized by priority (High/Low)?

### Decision
Use **keyword-based rules + VIP sender list** (configurable in YAML config).

### Rationale
- **Simple**: Easy to understand, debug, and adjust
- **Transparent**: User can see why an email was classified as High/Low
- **Configurable**: VIP list and keywords can be updated without code changes
- **Fast**: No ML inference latency, instant classification

### Implementation Pattern
```yaml
# config/triage_rules.yaml
priority_keywords:
  high:
    - urgent
    - asap
    - invoice
    - payment
    - emergency
    - action required
  low:
    - newsletter
    - notification
    - update
    - digest

vip_senders:
  - client@company.com
  - partner@business.com
  - boss@company.com
```

```python
def classify_priority(sender: str, subject: str, keywords_config: dict) -> str:
    subject_lower = subject.lower()
    
    # VIP sender → High priority
    if sender in keywords_config['vip_senders']:
        return 'high'
    
    # High-priority keywords
    for keyword in keywords_config['priority_keywords']['high']:
        if keyword in subject_lower:
            return 'high'
    
    # Low-priority keywords
    for keyword in keywords_config['priority_keywords']['low']:
        if keyword in subject_lower:
            return 'low'
    
    # Default: normal priority
    return 'normal'
```

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| ML classifier (Naive Bayes, etc.) | Learns from user behavior, improves over time | Training data needed, complex, opaque decisions | Overkill for Phase 2; simple rules sufficient |
| Manual classification only | Full user control | Defeats automation purpose, time-consuming | Violates "auto-triage" requirement |
| Sender-domain based | Simple (e.g., all @client.com = high) | Too coarse (misses context in subject) | Keyword + VIP more accurate |

---

## 4. HITL Enforcement Mechanism

**Question**: How should HITL (Human-in-the-Loop) approval be enforced for LinkedIn posts?

### Decision
Use **folder-based gate**: LinkedIn publisher only checks and publishes from `/Approved` folder.

### Rationale
- **Leverages Phase 1 workflow**: No new infrastructure needed
- **Physical gate**: File must be moved (atomic operation) - cannot bypass via metadata flag
- **Clear UX**: User knows exactly what to do (move to /Approved)
- **Audit-friendly**: Folder move is logged, creates clear audit trail

### Implementation Pattern
```python
def check_approved_posts():
    """Check /Approved folder for posts ready to publish."""
    approved_path = VAULT_ROOT / 'Approved'
    
    for post_file in approved_path.glob('linkedin-*.md'):
        metadata = parse_frontmatter(post_file.read_text())
        
        # Verify HITL approval
        if metadata.get('status') != 'approved':
            continue
        
        # Publish to LinkedIn
        publish_to_linkedin(metadata)
        
        # Move to /Done after publishing
        move_to_done(post_file)
```

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Metadata flag (hitl_approved: true) | Easier to implement (no file move) | Easier to bypass (accidental or intentional) | Folder gate is more robust |
| External approval system (web UI) | More professional UX | Additional infrastructure, complexity | Violates "file-based" principle |
| Email approval (reply to approve) | Convenient for user | Complex parsing, security concerns | Folder move is simpler and more secure |

---

## 5. Credential Management

**Question**: How should Gmail and LinkedIn credentials be stored and managed?

### Decision
Reuse **credentials.json** from Phase 1, stored in vault root (gitignored).

### Rationale
- **Consistent with Phase 1**: Same pattern, same location
- **Gitignored**: credentials.json in .gitignore (Phase 1)
- **Centralized**: All credentials in one place
- **OAuth2 compatible**: Supports token refresh flow

### Implementation Pattern
```python
# Gmail credentials
from google.oauth2.credentials import Credentials

def load_gmail_credentials():
    creds_path = VAULT_ROOT / 'credentials.json'
    if not creds_path.exists():
        raise FileNotFoundError("credentials.json not found. Please authenticate Gmail first.")
    
    creds = Credentials.from_authorized_user_file(creds_path)
    
    # Handle token expiry
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        # Save refreshed credentials
        with open(creds_path, 'w') as f:
            f.write(creds.to_json())
    
    return creds
```

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| Environment variables only | No file on disk | Hard to manage multiple tokens, not persistent | credentials.json more practical for OAuth2 |
| OS keychain (Windows Credential Manager) | Secure, OS-integrated | Platform-specific, complex code | credentials.json cross-platform |
| Encrypted file | More secure than plain JSON | Key management complexity, overkill for local vault | credentials.json gitignored is sufficient |

---

## 6. Email Deduplication Strategy

**Question**: How should duplicate emails be prevented (same email processed multiple times)?

### Decision
Track **Gmail message_id** in processed_emails.json log file.

### Rationale
- **Gmail-provided ID**: Unique per email, stable across API calls
- **Persistent log**: Survives restarts, crash recovery
- **Simple lookup**: O(1) check if message_id already processed
- **Audit-friendly**: Log includes when email was processed

### Implementation Pattern
```python
import json

PROCESSED_LOG = VAULT_ROOT / 'Logs' / 'processed_emails.json'

def load_processed_emails() -> set:
    if PROCESSED_LOG.exists():
        with open(PROCESSED_LOG, 'r') as f:
            data = json.load(f)
            return set(data.get('message_ids', []))
    return set()

def is_email_processed(message_id: str) -> bool:
    processed = load_processed_emails()
    return message_id in processed

def mark_email_processed(message_id: str):
    processed = load_processed_emails()
    processed.add(message_id)
    
    with open(PROCESSED_LOG, 'w') as f:
        json.dump({'message_ids': list(processed)}, f, indent=2)
```

### Alternatives Considered

| Alternative | Pros | Cons | Why Rejected |
|-------------|------|------|--------------|
| In-memory set | Fast, simple | Lost on restart → duplicates after reboot | Persistent log required |
| Database (SQLite) | Queryable, structured | Overkill for simple ID tracking | JSON file simpler |
| Filename-based dedup | No extra file | Fragile (filename changes), doesn't handle re-auth | Gmail message_id more reliable |

---

## Conclusion

All technical unknowns resolved. Key decisions:
1. **google-api-python-client** for Gmail (official, OAuth2 support)
2. **Playwright** for LinkedIn (no API approval needed, full functionality)
3. **Keyword + VIP rules** for priority classification (simple, transparent)
4. **Folder-based HITL gate** (/Approved folder only)
5. **credentials.json** for credential storage (consistent with Phase 1)
6. **processed_emails.json** for deduplication (persistent, simple)

Proceed to Phase 1: Generate data-model.md, contracts, and quickstart.md.
