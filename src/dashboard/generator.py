"""
Dashboard Generator for Digital FTE Vault.
Generates and updates the business dashboard with current status.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from ..config.settings import VAULT_ROOT, IN_PROGRESS_PATH


class DashboardGenerator:
    """Generator for Business Dashboard.md file."""
    
    def __init__(self):
        """Initialize dashboard generator."""
        self.dashboard_path = VAULT_ROOT / 'Dashboard.md'
    
    def get_active_projects(self) -> List[Dict[str, str]]:
        """
        Get active projects from /In_Progress folder.
        
        Returns:
            List of project dictionaries with name, status, next_action
        """
        projects = []
        
        if not IN_PROGRESS_PATH.exists():
            return projects
        
        # Scan /In_Progress for agent folders
        for agent_dir in IN_PROGRESS_PATH.iterdir():
            if agent_dir.is_dir():
                # Count tasks per agent
                task_count = len(list(agent_dir.glob('*.md')))
                if task_count > 0:
                    projects.append({
                        'name': agent_dir.name.replace('-', ' ').title(),
                        'status': 'In_Progress',
                        'next_action': f'{task_count} active task(s)',
                        'last_updated': datetime.now().strftime('%Y-%m-%d'),
                    })
        
        return projects
    
    def generate_dashboard(
        self,
        bank_balance: Optional[str] = None,
        gmail_unread: int = 0,
        whatsapp_unread: int = 0,
        manual_entry: bool = True,
    ) -> str:
        """
        Generate complete Dashboard.md content.
        
        Args:
            bank_balance: Current balance string (e.g., "$5,432.10")
            gmail_unread: Count of unread Gmail messages
            whatsapp_unread: Count of unread WhatsApp messages
            manual_entry: If True, mark data as manually entered
            
        Returns:
            Complete Markdown dashboard content
        """
        now = datetime.now().strftime('%Y-%m-%d %I:%M %p')
        
        # Get active projects
        projects = self.get_active_projects()
        
        # Build projects table
        if projects:
            projects_table = "| Project | Status | Next Action | Last Updated |\n"
            projects_table += "|---------|--------|-------------|--------------|\n"
            for proj in projects:
                projects_table += f"| {proj['name']} | {proj['status']} | {proj['next_action']} | {proj['last_updated']} |\n"
        else:
            projects_table = """| Project | Status | Next Action | Last Updated |
|---------|--------|-------------|--------------|
| [Add Project] | Waiting | Define first task | """ + now.split()[0] + " |"
        
        # Build dashboard content
        dashboard = f"""# Business Dashboard

**Last Updated**: {now}
**Phase**: 1 (Foundation) - {'Manual Entry' if manual_entry else 'Auto-Updated'}

---

## 📊 Bank Balance

> **Note**: Phase 1 - Manual entry. Phase 2+ will automate from bank API.

- **Current Balance**: {bank_balance or '$X,XXX.XX USD'}
- **Last Updated**: {now}
- **Last Transaction**: YYYY-MM-DD (Description - $Amount)

---

## 📬 Pending Messages

> **Note**: Phase 1 - Manual count. Phase 2+ will auto-count from Gmail/WhatsApp.

- **Gmail**: {gmail_unread} unread
- **WhatsApp**: {whatsapp_unread} unread
- **Last Checked**: {now}

---

## 🏗️ Active Projects

{projects_table}

### Status Definitions

- **In_Progress**: Actively being worked on
- **Waiting**: Waiting on external party (client, vendor, etc.)
- **Blocked**: Cannot proceed due to obstacle

---

## Quick Links

- [Dashboard.md](./Dashboard.md) - This file
- [Company_Handbook.md](./Company_Handbook.md) - AI rules and guidelines
- [/Inbox](./Inbox/) - Drop files here for processing
- [/Needs_Action](./Needs_Action/) - Pending tasks
- [/In_Progress](./In_Progress/) - Active tasks
- [/Approved](./Approved/) - Awaiting human approval
- [/Done](./Done/) - Completed tasks
- [/Logs](./Logs/) - Audit logs

---

## Phase 2+ Roadmap

### Planned Automations

- [ ] **Bank Balance**: Auto-fetch from Odoo/bank API
- [ ] **Pending Messages**: Auto-count from Gmail/WhatsApp watchers
- [ ] **Active Projects**: Auto-populate from `/In_Progress` folder metadata
- [ ] **Refresh Rate**: Auto-update every 5 minutes
"""
        
        return dashboard
    
    def write_dashboard(self, content: str) -> Path:
        """
        Write dashboard content to file.
        
        Args:
            content: Dashboard Markdown content
            
        Returns:
            Path to written file
        """
        with open(self.dashboard_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[Dashboard] Written to {self.dashboard_path}")
        return self.dashboard_path
    
    def update_dashboard(
        self,
        bank_balance: Optional[str] = None,
        gmail_unread: int = 0,
        whatsapp_unread: int = 0,
    ) -> Path:
        """
        Update dashboard with new data and write to file.
        
        Args:
            bank_balance: Current balance string
            gmail_unread: Gmail unread count
            whatsapp_unread: WhatsApp unread count
            
        Returns:
            Path to updated dashboard file
        """
        content = self.generate_dashboard(
            bank_balance=bank_balance,
            gmail_unread=gmail_unread,
            whatsapp_unread=whatsapp_unread,
        )
        return self.write_dashboard(content)


def create_initial_dashboard() -> Path:
    """Create initial Dashboard.md with placeholder data."""
    generator = DashboardGenerator()
    content = generator.generate_dashboard(manual_entry=True)
    return generator.write_dashboard(content)


if __name__ == '__main__':
    create_initial_dashboard()
