# LangGraph Humanitarian Report Agent

Autonomous agent that fetches live humanitarian data, analyzes it, and generates structured risk reports — built with LangGraph and Anthropic Claude.

## Status: 🚧 In Development

---

## What This Project Does

This agent runs an end-to-end pipeline with no human in the loop:

1. **Fetches** live data from humanitarian APIs (OCHA HDX, ReliefWeb)
2. **Analyzes** the data for patterns, trends, and risk indicators
3. **Generates** a structured report (markdown/PDF) summarizing findings

It's the agentic counterpart to [RAG-Humanitarian-risk-analysis-india](https://github.com/Ifsaurabh/RAG-Humanitarian-risk-analysis-India) — that project answers questions over a static knowledge base; this one autonomously acts on live data.

---

## Why This Project

Three things this demonstrates that a RAG project doesn't:
- **Tool calling** — the LLM decides when and how to invoke external APIs
- **Autonomous multi-step workflows** — no fixed query/response; the agent plans and executes a sequence of steps
- **Live, real-world data integration** — output reflects current conditions, not a frozen dataset

---

## Tech Stack

| Component | Tool |
|---|---|
| Agent orchestration | LangGraph (StateGraph, nodes, conditional edges) |
| LLM | Anthropic Claude (Haiku) |
| Serving | FastAPI |
| Data source 1 | OCHA HDX API (food prices, poverty indicators) |
| Data source 2 | ReliefWeb API (live situation reports) — pending appname approval |

---

## Architecture

agent/

├── tools/          # Data-fetching tools (HDX, ReliefWeb)

│   └── hdx_tool.py

├── graph.py         # LangGraph StateGraph — wires nodes together

└── state.py         # Shared state schema passed between nodes

main.py               # FastAPI entry point

---

## How It Works (Flow)

[Start]

│

▼

[Fetch Node] ──► calls HDX/ReliefWeb tools to get live data

│

▼

[Analysis Node] ──► processes data, identifies patterns/risk signals

│

▼

[Report Generation Node] ──► produces structured markdown report

│

▼

[End]


Each node reads from and writes to a shared `state` object (LangGraph pattern from Section 12 — same pattern used in the earlier Earthquake Report Generator build).

---

## Design Principle: Live & Dynamic Data

Tools resolve the **current** data source at call time rather than using hardcoded snapshots:

- The HDX tool queries `package_show` on the HDX CKAN API to find the dataset's *latest* resource URL dynamically — if the upstream provider updates the file, the agent picks up the new version automatically, with no code change required.
- ReliefWeb's `/v2/reports` endpoint is inherently live — always returns the most recent reports for a given filter.

This ensures the agent's reports reflect real-time conditions, not a point-in-time snapshot.

---

## Progress

## Progress
- [x] Project skeleton + repo setup
- [x] HDX tool — dynamic dataset resolver (`fetch_hdx_data`)
- [x] HDX tool — CSV loader (`load_hdx_csv`)
- [x] Query tool — filter/aggregate data (`query_data`)
- [ ] ReliefWeb tool (pending API appname approval)
- [x] LangGraph state schema
- [ ] Analysis node
- [ ] Report generation node
- [ ] FastAPI endpoint
- [ ] README — usage instructions + demo

---

## Related Projects
- [RAG-Humanitarian-risk-analysis-india](https://github.com/Ifsaurabh/RAG-Humanitarian-risk-analysis-India) — Project 1, RAG-based Q&A system