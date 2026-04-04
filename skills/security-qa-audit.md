# Security QA Audit Skill

## Purpose
QA and Security skill for Human-in-the-Loop (HITL) compliance. Validates that sensitive actions (payments, public posts) are moved to `/Approved/` before execution. Maintains daily JSON audit logs.

## Capabilities

### HITL Gate Enforcement
```python
from enum import Enum
from typing import List, Dict, Any

class SensitivityLevel(Enum):
    LOW = "low"           # Internal notes, file organization
    MEDIUM = "medium"     # Email replies, internal communications
    HIGH = "high"         # Payments, public posts, legal documents
    CRITICAL = "critical" # API keys, credentials, PII

class HITLValidator:
    SENSITIVE_ACTIONS = {
        "payment": SensitivityLevel.HIGH,
        "public_post": SensitivityLevel.HIGH,
        "invoice_generation": SensitivityLevel.HIGH,
        "credential_access": SensitivityLevel.CRITICAL,
        "email_reply": SensitivityLevel.MEDIUM,
        "file_move": SensitivityLevel.LOW,
    }
    
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.approved_folder = f"{vault_path}/Approved"
        self.audit_logger = AuditLogger(vault_path)
    
    def validate_action(self, action: Dict[str, Any]) -> ValidationResult:
        """Validate if action requires HITL approval."""
        action_type = action.get('type')
        sensitivity = self.SENSITIVE_ACTIONS.get(action_type, SensitivityLevel.LOW)
        
        if sensitivity in [SensitivityLevel.HIGH, SensitivityLevel.CRITICAL]:
            # Must be in /Approved/ folder
            if not self._is_in_approved_folder(action['file_path']):
                return ValidationResult(
                    approved=False,
                    reason=f"Action '{action_type}' requires HITL approval",
                    required_action="move_to_approved",
                    sensitivity=sensitivity.value
                )
        
        # Log all actions
        self.audit_logger.log(action, sensitivity)
        
        return ValidationResult(approved=True, sensitivity=sensitivity.value)
    
    def _is_in_approved_folder(self, file_path: str) -> bool:
        return "/Approved/" in file_path or file_path.startswith("Approved/")
```

### Audit Log Structure
```json
{
  "date": "2026-03-28",
  "vault_id": "AI_Employee_vault",
  "entries": [
    {
      "timestamp": "2026-03-28T10:30:00Z",
      "action_id": "act_20260328_103000_001",
      "action_type": "email_reply",
      "file_path": "/In_Progress/email-agent/reply-to-acme.md",
      "agent": "email-agent",
      "sensitivity": "medium",
      "hitl_required": false,
      "hitl_approved": null,
      "status": "completed",
      "metadata": {
        "recipient": "contact@acme.com",
        "subject": "Re: Project Update"
      }
    },
    {
      "timestamp": "2026-03-28T11:00:00Z",
      "action_id": "act_20260328_110000_002",
      "action_type": "payment",
      "file_path": "/Approved/invoice-payment-001.md",
      "agent": "accounting-agent",
      "sensitivity": "high",
      "hitl_required": true,
      "hitl_approved": {
        "approved_by": "user",
        "approved_at": "2026-03-28T11:15:00Z",
        "method": "file_move_to_approved"
      },
      "status": "pending_execution",
      "metadata": {
        "amount": 1500.00,
        "currency": "USD",
        "recipient": "Vendor LLC",
        "invoice_id": "INV-2026-0045"
      }
    }
  ],
  "summary": {
    "total_actions": 15,
    "hitl_required": 3,
    "hitl_approved": 2,
    "hitl_pending": 1,
    "blocked": 0
  }
}
```

### Daily Audit Log File
- Location: `/audit/2026-03-28.json`
- Created automatically at midnight or on first action
- Append-only during the day
- Sealed at EOD with hash for integrity

### Audit Log Sealing
```python
import hashlib
import json

def seal_audit_log(log_path: str) -> Dict:
    """Seal daily audit log with integrity hash."""
    with open(log_path, 'r') as f:
        content = f.read()
    
    # Create SHA-256 hash
    content_hash = hashlib.sha256(content.encode()).hexdigest()
    
    # Append seal metadata
    seal = {
        "sealed_at": datetime.now().isoformat(),
        "content_hash": content_hash,
        "entry_count": len(json.loads(content)['entries'])
    }
    
    # Write seal to separate file
    seal_path = log_path.replace('.json', '.seal.json')
    with open(seal_path, 'w') as f:
        json.dump(seal, f, indent=2)
    
    return seal
```

### Sensitive Action Detection
```python
def detect_sensitive_content(content: str, metadata: Dict) -> SensitivityLevel:
    """Analyze content for sensitivity indicators."""
    indicators = {
        SensitivityLevel.CRITICAL: [
            r'password\s*[=:]\s*\S+',
            r'api[_-]?key\s*[=:]\s*\S+',
            r'secret\s*[=:]\s*\S+',
            r'token\s*[=:]\s*\S+',
            r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b',  # Credit card
        ],
        SensitivityLevel.HIGH: [
            r'\$\d{4,}',  # Large amounts
            r'payment\s+of',
            r'invoice\s+payment',
            r'bank\s+transfer',
            r'public\s+post',
            r'press\s+release',
        ],
        SensitivityLevel.MEDIUM: [
            r'confidential',
            r'internal\s+only',
            r'nda',
            r'non[- ]?disclosure',
        ]
    }
    
    text = f"{content}\n{json.dumps(metadata)}".lower()
    
    for level, patterns in indicators.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                return level
    
    return SensitivityLevel.LOW
```

### Approval Workflow
```markdown
## HITL Approval Process

### 1. Agent Creates Action
- Agent completes task in `/In_Progress/{agent}/`
- Agent detects sensitive action (payment, public post)
- Agent moves file to `/Approved/` with prefix `pending_`

### 2. Human Review
- User reviews files in `/Approved/pending_*`
- User examines action details, metadata, intended outcome
- User approves by:
  - Renaming: `pending_invoice-payment.md` → `approved_invoice-payment.md`
  - Or adding frontmatter: `human_approved: true`

### 3. Agent Execution
- Agent polls `/Approved/approved_*` files
- Agent executes approved action
- Agent moves to `/Done/{YYYY-MM}/` after completion
- Agent logs completion in audit

### 4. Rejection Path
- User rejects by moving to `/Needs_Action/rejected/`
- User adds comment explaining rejection
- Agent notified, logs rejection in audit
```

### Approval File Template
```markdown
---
action_type: payment
sensitivity: high
created_by: accounting-agent
created_at: 2026-03-28T11:00:00Z
status: pending_approval
---

# Payment Approval Request

## Action Details
- **Type**: Invoice Payment
- **Amount**: $1,500.00 USD
- **Recipient**: Vendor LLC
- **Invoice**: INV-2026-0045
- **Due Date**: 2026-04-05

## Justification
Payment for Q1 consulting services as per contract #2026-001.

## Supporting Documents
- [invoice-2026-0045.pdf](./attachments/invoice-2026-0045.pdf)
- [contract-2026-001.pdf](./attachments/contract-2026-001.pdf)

---

## Human Approval
<!-- User: Change status to 'approved' and move to Approved/ when ready -->
- [ ] Approved
- [ ] Rejected

**Comments**: 
```

### Compliance Reports
```python
def generate_compliance_report(period: str) -> Dict:
    """Generate weekly/monthly compliance report."""
    audit_files = get_audit_files_for_period(period)
    
    total_actions = 0
    hitl_required = 0
    hitl_approved = 0
    blocked_attempts = 0
    avg_approval_time = []
    
    for log in audit_files:
        for entry in log['entries']:
            total_actions += 1
            if entry['hitl_required']:
                hitl_required += 1
                if entry['hitl_approved']:
                    hitl_approved += 1
                    # Calculate approval time
                    created = datetime.fromisoformat(entry['timestamp'])
                    approved = datetime.fromisoformat(entry['hitl_approved']['approved_at'])
                    avg_approval_time.append((approved - created).total_seconds())
            if entry['status'] == 'blocked':
                blocked_attempts += 1
    
    return {
        "period": period,
        "total_actions": total_actions,
        "hitl_required": hitl_required,
        "hitl_approved": hitl_approved,
        "compliance_rate": hitl_approved / hitl_required if hitl_required > 0 else 1.0,
        "blocked_attempts": blocked_attempts,
        "avg_approval_time_seconds": sum(avg_approval_time) / len(avg_approval_time) if avg_approval_time else 0,
        "recommendations": generate_compliance_recommendations(...)
    }
```

## Configuration
```yaml
security:
  hitl_required_for:
    - payment
    - public_post
    - invoice_generation
    - credential_access
  
  audit:
    log_path: "./audit"
    daily_seal: true
    retention_days: 365
  
  alerts:
    blocked_action: true
    critical_sensitivity: true
    approval_timeout_hours: 24
```

## Error Handling
- Audit log write failure: Retry, then alert user
- Hash mismatch on seal: Log security incident
- Approval timeout: Notify user of pending items
- Unauthorized file access: Block and alert

## Security
- Audit logs are append-only
- Daily seals prevent tampering
- Never store credentials in audit logs (mask PII)
- Access control: Only user can approve, agents can only request
- Encryption at rest for audit files
