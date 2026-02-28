# 🌍 The Decarbonization Stack: AI Agent Engine

An autonomous multi-agent system designed to identify market gaps in the renewable energy sector and generate compelling startup pitches. This project is built to run **entirely locally** on Apple Silicon (M1/M2/M3) for maximum privacy and zero API costs.

---

## 🚀 The Architecture
This application uses **CrewAI** to orchestrate two specialized AI agents:
1. **The Climate Tech Researcher:** Scans the renewable energy landscape (via DuckDuckGo) to identify 2026 market gaps and inconsistencies.
2. **The Startup Technical Writer:** Translates technical data into professional project pitches tailored for a Data Engineering audience.



## 🛠️ Tech Stack
- **Framework:** CrewAI (Multi-agent orchestration)
- **Local Brain:** Ollama running Llama 3
- **UI:** Streamlit (Interactive Web Dashboard)
- **Bridge:** LiteLLM (Universal model translator)
- **Search:** DuckDuckGo Search (Live web scraping)

## 📦 Installation & Setup

### 1. Prerequisites
- **Ollama:** Install from [ollama.com](https://ollama.com)
- **Model:** Run `ollama run llama3` in your terminal.

### 2. Environment Setup
```bash
git clone <YOUR_GITHUB_LINK_HERE>
cd agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt