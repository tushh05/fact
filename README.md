# 🔍 TruthLayer: Multi-Agent AI Fact-Checking Engine

> **AI Engineering Project** | Real-Time Verification Engine

**TruthLayer** is an asynchronous multi-agent AI verification system designed to combat misinformation. By utilizing the Gemini Framework alongside live web search capabilities, it automatically parses statements, extracts key claims, and cross-references them against trusted web documentation layers in real-time.

---

## 🔑 Key Features & Highlights

- **Asynchronous Multi-Agent Pipeline:** Orchestrated agents using the Gemini framework to analyze context, isolate claims, and loop Regex patterns for extraction.
- **Live Web Verification:** Integrated Serper API client to dynamically query live web layers and establish factual benchmarks.
- **Automated Benchmarking:** Cross-checks claims against high-credibility web documentation with factual confidence scoring.
- **Interactive UI Dashboard:** Built-in Streamlit UI for seamless query input, pipeline execution logs, and output visualizer.

---

## 🛠️ Tech Stack & Architecture

- **Core Language:** Python
- **AI / LLM Framework:** Gemini Framework & API
- **Web Search & Indexing:** Serper API Client
- **User Interface:** Streamlit
- **Parsing & Logic:** Regex, Asynchronous Execution Loops (asyncio)

---

## 📂 Repository Structure

```text
├── agents/             # Multi-agent prompt definitions & pipeline logic
├── src/
│   ├── parsing.py      # Regex extraction & text parsing engine
│   ├── verification.py # Serper API integration & cross-referencing
│   └── dashboard.py    # Streamlit UI interface
├── config.py           # API keys & configuration setup
├── requirements.txt    # Python dependencies
└── README.md
