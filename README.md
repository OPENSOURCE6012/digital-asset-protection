# 🛡️ Digital Asset Protection System

<div align="center">

![Google ADK](https://img.shields.io/badge/Google%20ADK-Multi--Agent-4285F4?style=for-the-badge&logo=google&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini%202.5%20Flash-AI%20Model-34A853?style=for-the-badge&logo=google&logoColor=white)
![Cloud Run](https://img.shields.io/badge/Cloud%20Run-Deployed-EA4335?style=for-the-badge&logo=google-cloud&logoColor=white)
![Python](https://img.shields.io/badge/Python%203.12-Language-FBBC05?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Container-0EA5E9?style=for-the-badge&logo=docker&logoColor=white)

**An AI-powered multi-agent platform for sports media rights protection**

Built for **Google Gen AI Academy APAC Edition 2026 — Solution Challenge**

[🚀 Live Demo](https://my-agents-807379743631.us-central1.run.app/dev-ui/?app=digital_asset_app) · [📦 GitHub](https://github.com/OPENSOURCE6012/sports-asset-protection) · [👤 LinkedIn](https://www.linkedin.com/in/banty-raj-032170267)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Problem Statement](#-problem-statement)
- [Solution](#-solution)
- [Architecture](#-architecture)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Setup & Deployment](#-setup--deployment)
- [Agent Tools](#-agent-tools)
- [Usage Examples](#-usage-examples)
- [Live Demo](#-live-demo)
- [Author](#-author)

---

## 🌟 Overview

The **Digital Asset Protection System** is a production-grade, multi-agent AI application that enables sports media rights holders to:

- **Register** official sports media assets (videos, images, audio, documents)
- **Detect & Flag** IP violations with severity classification
- **Search** violations by keyword, asset ID, or owner
- **Generate** full protection reports for single assets or entire portfolios
- **Manage** asset lifecycle statuses in real time

All interactions happen through **natural language** — rights holders simply describe what they need, and the Gemini-powered agent system handles the rest.

---

## ❗ Problem Statement

Sports media rights are routinely violated through:
- Unauthorized live streaming of matches and events
- Piracy and redistribution of licensed video content
- Unauthorized use of sports imagery and audio

Rights holders currently lack a unified, intelligent system to register, monitor, flag, and report IP violations in real time — resulting in massive revenue loss and unenforceable licensing agreements.

---

## ✅ Solution

A **multi-agent AI system** built with Google ADK that coordinates 3 specialist agents:

```
User (Natural Language)
        ↓
Root Agent — Coordinator (Gemini 2.5 Flash)
        ↓
┌───────────────────┬──────────────────────┬─────────────────┐
│  Registration     │  Violation Detection │  Report Agent   │
│  Agent            │  Agent               │                 │
│                   │                      │                 │
│  register_asset   │  flag_violation      │  get_asset_     │
│  list_assets      │  search_violations   │  report         │
│  update_status    │                      │                 │
└───────────────────┴──────────────────────┴─────────────────┘
        ↓
Google Cloud Run · Vertex AI · MCP Toolbox
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User / Browser                        │
└──────────────────────────┬──────────────────────────────┘
                           │ HTTPS
┌──────────────────────────▼──────────────────────────────┐
│          Google Cloud Run (my-agents service)            │
│         ADK Web Server · Python 3.12 · Docker            │
│                                                          │
│  ┌───────────────────────────────────────────────────┐   │
│  │        Root Agent — digital_asset_coordinator     │   │
│  │              Model: gemini-2.5-flash               │   │
│  │                                                   │   │
│  │  ┌──────────────┐ ┌───────────────┐ ┌──────────┐ │   │
│  │  │ Registration │ │   Violation   │ │  Report  │ │   │
│  │  │    Agent     │ │    Agent      │ │  Agent   │ │   │
│  │  └──────┬───────┘ └──────┬────────┘ └────┬─────┘ │   │
│  └─────────┼────────────────┼───────────────┼───────┘   │
│            ↓                ↓               ↓            │
│  ┌─────────────────────────────────────────────────┐    │
│  │               6 Python Tool Functions            │    │
│  │  register_asset · list_assets · update_status    │    │
│  │  flag_violation · search_violations · get_report │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
   Vertex AI /       MCP Toolbox        BigQuery
   Gemini API        SQL Tools          Datasets
```

---

## 🎯 Features

| Feature | Description |
|---|---|
| 🗂️ **Asset Registration** | Register sports media assets with ID, name, type, owner, and license expiry |
| 📋 **Asset Listing** | View all registered assets with current status |
| 🚨 **Violation Flagging** | Flag unauthorized usage with URL, description, and severity (low/medium/high/critical) |
| 🔍 **Violation Search** | Search by keyword, asset ID, owner, severity, or source URL |
| 📊 **Protection Reports** | Per-asset or full portfolio reports with violation breakdown |
| 🔄 **Status Management** | Update asset lifecycle: active → archived → pending_review → suspended |
| 🤖 **Natural Language** | All operations via conversational AI — no technical knowledge required |
| ⚡ **Graceful Degradation** | Agent stays alive even if toolbox connection fails |
| 🔐 **Dual Auth** | Supports both Vertex AI (service account) and Gemini API key |

---

## 🛠️ Tech Stack

| Technology | Purpose | Version |
|---|---|---|
| **Google ADK** | Multi-agent orchestration framework | Latest |
| **Gemini 2.5 Flash** | LLM for reasoning & tool selection | gemini-2.5-flash |
| **Vertex AI** | Managed AI auth & platform | — |
| **MCP Toolbox** | SQL tools exposed as agent tools | Latest |
| **Google Cloud Run** | Serverless container deployment | — |
| **Python** | Agent code & tool functions | 3.12 |
| **Docker** | Containerized build & deploy | — |
| **BigQuery** | Public datasets & persistent storage | — |

---

## 📁 Project Structure

```
sports-asset-protection/
│
├── my-agents/
│   ├── digital_asset_app/
│   │   ├── agent.py          # ← Main agent file (root + 3 sub-agents + 6 tools)
│   │   ├── __init__.py
│   │   └── __pycache__/
│   ├── Dockerfile            # Container build config
│   └── requirements.txt      # Python dependencies
│
├── mcp-toolbox/
│   ├── Dockerfile
│   ├── toolbox               # MCP Toolbox binary
│   └── tools.yaml            # Tool definitions (register_asset, etc.)
│
└── README.md
```

---

## 🚀 Setup & Deployment

### Prerequisites

- Google Cloud account with billing enabled
- `gcloud` CLI installed
- Docker installed
- Python 3.12+

### 1. Clone the Repository

```bash
git clone https://github.com/OPENSOURCE6012/sports-asset-protection.git
cd sports-asset-protection/my-agents
```

### 2. Set Environment Variables

```bash
# Option A — Vertex AI (recommended on GCP)
export GOOGLE_GENAI_USE_VERTEXAI=true
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=us-central1

# Option B — Gemini API Key
export GOOGLE_API_KEY=your-key-from-aistudio.google.com

# Optional — MCP Toolbox
export TOOLBOX_URL=http://your-toolbox-host:port
```

### 3. Install Dependencies

```bash
pip install google-adk toolbox-core google-cloud-aiplatform
```

### 4. Run Locally

```bash
adk web
# Open: http://localhost:8000/dev-ui/?app=digital_asset_app
```

### 5. Deploy to Cloud Run

```bash
# Enable required APIs
gcloud services enable run.googleapis.com aiplatform.googleapis.com

# Deploy
gcloud run deploy my-agents \
  --source . \
  --region=us-central1 \
  --allow-unauthenticated \
  --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=true,GOOGLE_CLOUD_PROJECT=your-project-id,GOOGLE_CLOUD_LOCATION=us-central1"
```

### 6. Grant Vertex AI Permissions

```bash
# Get Cloud Run service account
SA=$(gcloud run services describe my-agents \
  --region=us-central1 \
  --format="value(spec.template.spec.serviceAccountName)")

# Grant Vertex AI user role
gcloud projects add-iam-policy-binding your-project-id \
  --member="serviceAccount:$SA" \
  --role="roles/aiplatform.user" \
  --condition=None
```

---

## 🔧 Agent Tools

### Tool Reference

```python
# Tool 1 — Register a new asset
register_asset(
    asset_id="ESPN-WC2024-001",
    asset_name="FIFA World Cup 2024 Highlights",
    asset_type="Video",           # Video | Image | Audio | Document
    owner="ESPN",
    license_expiry="2025-12-31"
)

# Tool 2 — List all registered assets
list_assets()

# Tool 3 — Update asset lifecycle status
update_asset_status(
    asset_id="ESPN-WC2024-001",
    new_status="archived"         # active | archived | pending_review | suspended
)

# Tool 4 — Flag an IP violation
flag_violation(
    asset_id="ESPN-WC2024-001",
    source_url="https://piracy-site.com/wc-stream",
    description="Unauthorized live rebroadcast of World Cup match",
    severity="critical"           # low | medium | high | critical
)

# Tool 5 — Search violations
search_violations(query="ESPN")   # Searches by keyword, asset ID, URL, severity

# Tool 6 — Generate protection report
get_asset_report(asset_id="ALL")  # "ALL" for full portfolio, or specific asset ID
```

---

## 💬 Usage Examples

Once deployed, open the ADK Web UI and try these natural language prompts:

```
"Register a new asset: NBA Finals 2024 broadcast, owned by TNT, video, license until 2026-06-01"

"List all registered assets"

"Flag a critical violation — youtube.com/watch?v=abc123 is streaming our World Cup content"

"Search for all ESPN violations"

"Generate the full portfolio protection report"

"Update ESPN-WC2024-001 status to archived"
```

---

## 🌐 Live Demo

| Link | Description |
|---|---|
| [ADK Web UI](https://my-agents-807379743631.us-central1.run.app/dev-ui/?app=digital_asset_app) | Full agent interface with Events & Traces |
| [Direct Agent URL](https://my-agents-807379743631.us-central1.run.app) | Production Cloud Run service |
| [GitHub](https://github.com/OPENSOURCE6012/sports-asset-protection) | Source code |

---

## 🐛 Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| `TOOLBOX_URL is not set` | Missing env var | Set `TOOLBOX_URL` in Cloud Run or run without toolbox |
| `No API key provided` | Missing auth | Set `GOOGLE_GENAI_USE_VERTEXAI=true` or `GOOGLE_API_KEY` |
| `No invocations found` | Agent crash at startup | Check Cloud Run logs for startup errors |
| `Task exception was never retrieved` | Cascading from auth error | Fix auth first, this auto-resolves |
| `Service account does not exist` | Wrong SA in IAM command | Run `gcloud run services describe` to get real SA |

---

## 📈 Future Roadmap

- [ ] **Phase 1** — BigQuery integration for persistent asset & violation storage
- [ ] **Phase 2** — Automated web scanning sub-agent using Google Search API
- [ ] **Phase 3** — React dashboard with violation heatmaps and asset health scores
- [ ] **Phase 4** — REST API + webhook alerts for critical violations
- [ ] **Phase 5** — Expand from sports IP to music, film, and publishing rights

---

## 👤 Author

**Banty Raj**
- 📧 Email: rajbanty388@gmail.com
- 📱 Phone: 8084535149
- 💼 LinkedIn: [banty-raj-032170267](https://www.linkedin.com/in/banty-raj-032170267)
- 🐙 GitHub: [OPENSOURCE6012](https://github.com/OPENSOURCE6012)
- 📍 Patna, Bihar, India

**Education:** B.Tech in Electrical & Electronics Engineering
**College:** Bakhtiyarpur College of Engineering, Bihar Engineering University (2022–2026)

**Hackathon:** Google Gen AI Academy APAC Edition 2026
- Selected participant building production-grade AI agents
- Built 4+ multi-agent systems on Google Cloud Run
- Diagnosed and resolved 15+ production Cloud Run, BigQuery, Docker, and MCP Toolbox issues

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

Built with ❤️ using **Google ADK** · **Gemini 2.5 Flash** · **Google Cloud Run**

**Google Gen AI Academy APAC Edition 2026 — Solution Challenge**

</div>
