# 🤖 AI Employee Vault

> **An Autonomous Digital FTE** — Handles Social Media Marketing, Email Correspondence & Real-time Accounting in Odoo.

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-Automation-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev/)
[![Odoo](https://img.shields.io/badge/Odoo-17.0-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![AI Models](https://img.shields.io/badge/AI-Groq%20%7C%20Llama%203.3-FF6B35?style=for-the-badge&logo=openai&logoColor=white)](https://groq.com/)
[![License](https://img.shields.io/badge/License-MIT-00FF00?style=for-the-badge)](LICENSE)

</div>

---

## 📋 Executive Summary

**AI Employee Vault** transforms your workflow by deploying an **autonomous digital employee** that works 24/7. This isn't just a script—it's a full-stack automation system that:

- 📱 **Posts to Social Media** across LinkedIn, Facebook, Instagram & Twitter
- 📧 **Manages Email Correspondence** with AI-drafted replies
- 💰 **Tracks Finances in Real-time** via Odoo ERP integration
- 📊 **Generates CEO Briefings** with daily performance reports

Built with a **modular agent architecture**, each component operates independently while contributing to a seamless autonomous workflow.

---

## 🛠 The Tech Stack

| Layer | Technology | Purpose |
|:------|:-----------|:--------|
| **Core** | Python 3.10+ | Primary runtime environment |
| **Browser Automation** | Playwright | Cross-platform web interaction |
| **ERP Integration** | Odoo 17.0 (Docker) | Financial tracking & accounting |
| **AI Engine** | Groq / Llama 3.3 70B | Intelligent email drafting |
| **Containerization** | Docker Compose | Isolated, reproducible deployments |
| **Configuration** | Environment Variables | Secure credential management |

---

## 🔄 Autonomous Workflow: The 5-Step Process

<div align="center">

```
┌─────────────────────────────────────────────────────────────────────┐
│                     AI EMPLOYEE - CONTINUOUS CYCLE                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  1️⃣  MONITOR                                                         │
│     📧 Gmail Monitor → Fetches unread emails → /Needs_Action          │
│     ↓                                                                 │
│  2️⃣  REASON                                                          │
│     🤖 Auto-Drafter → Generates AI replies → /In_Progress             │
│     ↓                                                                 │
│  3️⃣  ACT                                                             │
│     📱 Social Orchestrator → Posts approved content → Odoo logging    │
│     ↓                                                                 │
│  4️⃣  DELIVER                                                         │
│     📤 Gmail Sender → Sends approved replies → Gmail                  │
│     ↓                                                                 │
│  5️⃣  REPORT                                                          │
│     📊 CEO Briefer → Updates daily metrics → CEO_Report.md            │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

</div>

Each cycle runs every **5 minutes**, ensuring continuous operation without manual intervention.

---

## 💰 Odoo Financial Integration

Every social media post automatically creates a **journal entry** in Odoo:

| Feature | Description |
|:--------|:------------|
| **Auto-Logging** | 500 PKR expense entry per post (configurable) |
| **Platform Tracking** | Breakdown by LinkedIn, Facebook, Twitter, Instagram |
| **Draft Entries** | Created as drafts for human review before posting |
| **Real-time Reports** | CEO briefings include budget analysis & recommendations |

**Example Journal Entry:**
```
Account: 500000 (Marketing Expense)
Debit: 500.00 PKR
Reference: "Social Post: facebook_test"
Status: Draft
```

---

## 🧩 System Architecture

| Module | Icon | Responsibility |
|:-------|:----:|:---------------|
| **Monitor** | 👁️ | Fetches new emails, detects social media tasks |
| **Reasoner** | 🧠 | AI-powered email drafting using LLM |
| **Actor** | ⚡ | Executes posts across all social platforms |
| **Accountant** | 💼 | Logs expenses to Odoo, tracks marketing spend |
| **Reporter** | 📊 | Generates CEO briefings with actionable insights |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Docker & Docker Compose** (for Odoo)
- **Playwright** (`playwright install chromium`)

### 1. Clone & Setup

```bash
git clone https://github.com/your-org/ai-employee-vault.git
cd ai-employee-vault
```

### 2. Configure Environment

```bash
# Copy the template
cp .env.example .env

# Edit with your credentials
nano .env  # or your preferred editor
```

**Required Variables:**
```env
# Odoo ERP
ODOO_URL=http://localhost:8069
ODOO_DB=odoo_vault
ODOO_USER=admin
ODOO_PASSWORD=your-password

# LinkedIn
LINKEDIN_EMAIL=your-email@example.com
LINKEDIN_PASSWORD=your-password

# Groq AI (for email drafting)
GROQ_API_KEY=your-api-key
```

### 3. Start Odoo (Docker)

```bash
docker-compose up -d
```

Verify at: `http://localhost:8069`

### 4. Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 5. Run the Autonomous Employee

```bash
# Start continuous automation loop
python main.py
```

**Output:**
```
╔==========================================================╗
║          AI EMPLOYEE - SOCIAL MEDIA CYCLE                   ║
║  Time: 2026-04-04 01:00:00                                ║
╚==========================================================╝

[Social Orchestrator] ✓ Completed successfully
[CEO Briefer] ✓ Completed successfully

Success: 2/2 steps completed
```

---

## 📁 Project Structure

```
AI_Employee_vault/
├── src/
│   ├── agent/          # 🧠 Auto-Drafter (AI email generation)
│   ├── config/         # ⚙️ Settings & environment
│   ├── gmail/          # 📧 Gmail Monitor & Sender
│   ├── linkedin/       # 💼 LinkedIn Poster
│   ├── skills/         # ⚡ Core automation skills
│   │   ├── odoo_manager.py      # 💼 Odoo integration
│   │   ├── social_orchestrator.py # 📱 Social media dispatcher
│   │   └── ceo_briefer.py       # 📊 Report generator
│   └── watcher/        # 👁️ File system monitors
├── Approved/           # ✅ Approved tasks ready for execution
├── Done/               # ✅ Completed tasks
├── Logs/               # 📝 Audit logs
├── .env                # 🔒 Credentials (gitignored)
├── .env.example        # 📋 Template
├── docker-compose.yml  # 🐳 Odoo + PostgreSQL
└── main.py             # 🚀 Master orchestrator
```

---

## 🔒 Security

- ✅ **No hardcoded credentials** — All secrets in `.env`
- ✅ **`.env` excluded from Git** — Never committed
- ✅ **Browser sessions isolated** — `.browser_data/` gitignored
- ✅ **Environment variables only** — `os.getenv()` throughout

Run security audit:
```bash
python test_security_audit.py
```

---

## 📊 Monitoring & Reports

Daily CEO briefings are automatically generated in `CEO_Report.md`:

```markdown
# CEO Daily Briefing Report

| Metric | Value |
|--------|-------|
| Total Posts Today | 3 |
| Total Budget Spent | 1,500.00 PKR |
| Average Cost Per Post | 500.00 PKR |

## Platform Breakdown
| Platform | Posts | Amount |
|----------|-------|--------|
| Facebook | 1 | 500.00 PKR |
| LinkedIn | 1 | 500.00 PKR |
| Twitter | 1 | 500.00 PKR |
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with ❤️ for autonomous digital workflows**

[![Made With Python](https://img.shields.io/badge/Made%20With-Python-FFD700?style=flat-square&logo=python)](https://www.python.org/)
[![Powered By Odoo](https://img.shields.io/badge/Powered%20By-Odoo-714B67?style=flat-square&logo=odoo)](https://www.odoo.com/)
[![AI-Enhanced](https://img.shields.io/badge/AI-Enhanced-FF6B35?style=flat-square)](https://groq.com/)

</div>
