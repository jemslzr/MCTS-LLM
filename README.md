# Stateful Multi-Turn Adversarial Search for Promptware Persistence in LLM Agent Workflows
---

## Overview

This project implements an **MCTS‑guided fuzzing framework** that discovers multi‑turn prompt injection vulnerabilities in LLM‑powered agents. The system simulates a realistic email‑assistant agent with memory (stateful) and tool‑calling capabilities. 

It uses Monte Carlo Tree Search (MCTS) pre‑training on the **NotInject** dataset to assign vulnerability weights to prompts, then adaptively injects stronger payloads into higher‑weight seeds during live evaluation.

**Key Result**: Achieved **48% Attack Success Rate (ASR)** against **Llama 3.3 70B** (via Groq) – a well‑aligned, enterprise‑scale LLM.

---

## Interpretation:
Higher MCTS weight correlates with higher actual vulnerability, confirming the effectiveness of the pre‑training. A 48% success rate against a modern 70B‑parameter LLM indicates that even well‑aligned agents are significantly susceptible to multi‑turn prompt injection.

---
## File Structure
.
├── app.py                      # Flask server (serves from cache)
├── precompute.py               # Offline LLM evaluation → results_cache.json
├── spade.html                  # Frontend layout
├── spade.css                   # Styling (dark/light, chat bubbles, metrics)
├── spade.js                    # Frontend logic (typing animation, filters, API)
├── trained_mcts_notinject.json # Seeds + MCTS weights (from training script)
├── results_cache.json          # Pre‑computed LLM responses (generated once)
└── README.md                   # Setup
## Setup
**Prerequisites**
Python 3.10+
Either Ollama (local, free) or Groq API key (cloud, fast)

**Installation**
```bash
git clone https://github.com/your-repo/spade-mcts.git
cd spade-mcts
python -m venv venv
source venv/bin/activate      # or .\venv\Scripts\activate (Windows)
# to get out of venv, "deactivate"
pip install flask flask-cors requests
```
**Run the web interface**
```bash
python app.py
```
Open http://localhost:5000 and click Run All or individual conversations.

### Optional
**API Key Setup**
This project requires a Groq API key (free) to pre‑compute results.
1. Get your API key from [console.groq.com](https://console.groq.com)
2. Copy and replace PUT_YOUR_API from precompute.py with your actual key.

Pre‑compute results (once, before presentation)
```bash

ollama pull llama3.2:3b
python precompute.py   # regenerates results_cache.json
```
This regenerates results_cache.json with authentic LLM responses for all 255 seeds.
## License
This project is released for academic and research purposes.

## Acknowledgments
NotInject dataset by Hao Li & Xiaogeng Liu
