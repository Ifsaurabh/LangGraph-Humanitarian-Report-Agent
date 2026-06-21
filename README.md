# LangGraph Humanitarian Report Agent

Autonomous agent that fetches live humanitarian data, analyzes it, and generates structured risk reports — built with LangGraph and Anthropic Claude.

## Status: ✅ Core Pipeline Complete

---

## What This Project Does

This agent runs an end-to-end pipeline with no human in the loop:

1. **Fetches** live data from humanitarian APIs (OCHA HDX, ReliefWeb)
2. **Analyzes** the data for patterns, trends, and risk indicators
3. **Generates** a structured report (markdown) summarizing findings
4. **Serves** the report via a REST API endpoint

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
| Agent orchestration | LangGraph (StateGraph, nodes, edges) |
| LLM | Anthropic Claude (Haiku) |
| Serving | FastAPI + uvicorn |
| Cloud storage | AWS S3 (boto3) |
| Data source 1 | OCHA HDX API (food prices, poverty indicators) |
| Data source 2 | ReliefWeb API (live situation reports) — pending appname approval |

---

## Architecture

```
project-root/
├── agent/
│   ├── graph.py
│   ├── state.py
│   └── tools/
│       ├── hdx_tool.py
│       ├── query_tool.py
│       └── tool_definitions.py
├── lang_food_poverty_output/    # sample generated reports
├── main.py
├── .env.example
├── requirements.txt
└── README.md
```

---

## How It Works (Flow)

```
[Start]
↓
[Data Gathering Node] — ReAct tool-calling loop
  LLM reads question, decides which tools to call
  Tools: get_food_price_data, get_poverty_data, query_data
↓
[Analysis Node]
  LLM reasons over gathered data
↓
[Report Generation Node]
  Produces structured markdown report
↓
[Save/Store Node]
  Saves locally + uploads to S3
↓
[END]
```

---

## API Usage

Start the server:
```bash
uvicorn main:app --reload
```

POST a question:
```bash
curl -X POST "http://localhost:8000/question" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the food security situation in Bihar?"}'
```

Interactive docs: `http://localhost:8000/docs`

**Optional: run with Docker instead**

```bash
docker compose up --build
```
This builds and runs the same app via the included `docker-compose.yml`, 
mapped to the same port 8000. Note: the live EC2 deployment described below 
actually runs via plain `uvicorn` + `nohup`, not Docker — this Compose 
file is provided as a convenient way to run the app locally without 
setting up a virtual environment.

---

## Sample Output

Query: *"What is the food security situation in Bihar?"*

The agent autonomously:
- Fetched live food price and poverty data from OCHA HDX
- Identified that 54.64% of Bihar's population is at food security risk
- Generated a structured report with risk assessment, severity table, and prioritized recommendations

---

## Demo - Screenshots

### Swagger UI
![Home](screenshots/01_swagger_home.png)

### Try it out
![Try it out](screenshots/02_tryout.png)

### Enter question
![Question](screenshots/03_question.png)

### Authorization — prompt
![Auth prompt](screenshots/04_auth_prompt.png)

### Authorization — credentials
![Auth credentials](screenshots/05_auth_credentials.png)

### Invalid credentials — 401
![Invalid credentials](screenshots/06_invalid_credentials.png)

### Successful response
![Response](screenshots/07_response.png)

## Design Principle: Live & Dynamic Data

Tools resolve the **current** data source at call time rather than using hardcoded snapshots:

- The HDX tool queries `package_show` on the HDX CKAN API to find the dataset's latest resource URL dynamically
- ReliefWeb's `/v2/reports` endpoint always returns the most recent reports

---

## Try It Live

A live demo is deployed on the same AWS EC2 instance as Project 1 (plain 
uvicorn, port 8000). Since this instance doesn't have an Elastic IP, 
confirm the current public IP before connecting (it changes on instance 
stop/start).

- **Swagger UI:** `http://<current-ec2-ip>:8000/docs`
- **Username:** `demo`
- **Password:** `demo-humanitarian-2026`

Open the link, click "Authorize" in Swagger UI, enter the credentials above, 
then try the `/question` endpoint with something like *"What is the food 
security situation in Bihar?"*

---

## Known Limitations & Production Considerations

- **HTTP only (no TLS):** This demo deployment runs over plain HTTP on a 
  single EC2 instance without a domain name. In production, this would be 
  addressed with a registered domain, Nginx as a reverse proxy, and 
  Let's Encrypt for free TLS certificates (via Certbot). Deferred here to 
  keep the deployment footprint minimal for a portfolio demo — the focus 
  of this project is the RAG/agent architecture, not infra hardening.
- **No Elastic IP:** Public IP changes on instance stop/start since this 
  is a cost-optimized t3.micro setup without a static IP allocation.

  ---

## Progress

- [x] Project skeleton + repo setup
- [x] HDX tool — dynamic dataset resolver
- [x] HDX tool — CSV loader
- [x] Query tool — filter/aggregate data
- [x] LangGraph state schema
- [x] Data gathering node — ReAct loop + parallel tool calls
- [x] Analysis node
- [x] Report generation node
- [x] Save/store node — local + S3 upload
- [x] FastAPI endpoint — POST /question
- [ ] ReliefWeb tool (pending API appname approval)
- [x] Basic authentication
- [x] Demo screenshots

---

## Related Projects
- [RAG-Humanitarian-risk-analysis-india](https://github.com/Ifsaurabh/RAG-Humanitarian-risk-analysis-India) — Project 1, RAG-based Q&A system
