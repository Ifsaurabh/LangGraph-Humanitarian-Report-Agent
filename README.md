# LangGraph Humanitarian Report Agent

Autonomous agent that fetches live humanitarian data (ReliefWeb, OCHA HDX), 
analyzes patterns, and generates structured risk reports — built with LangGraph 
and Anthropic Claude.

## Status:  In Development

## Planned Tech Stack
- LangGraph (agent orchestration)
- Anthropic Claude (Haiku)
- FastAPI (serving)
- ReliefWeb API + OCHA HDX (data sources)

## Architecture (planned)
- Data fetching tools (ReliefWeb, HDX)
- Analysis node
- Report generation node
- LangGraph state machine tying it together