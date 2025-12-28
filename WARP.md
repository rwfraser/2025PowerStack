# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a FastAPI-based AI agent API powered by LangGraph and OpenAI's GPT-4o model. The application exposes a simple chat endpoint that processes user messages through a LangGraph workflow.

## Architecture

### Core Components

- **main.py**: FastAPI application entry point
  - Defines the `/chat` POST endpoint
  - Handles request/response serialization via Pydantic models
  - Invokes the LangGraph agent asynchronously

- **agent.py**: LangGraph agent implementation
  - Defines `AgentState` as a TypedDict with message sequences
  - Creates a simple workflow with a single "agent" node that invokes ChatOpenAI (GPT-4o)
  - Compiles the StateGraph into an executable agent

### State Management

The agent uses LangGraph's `StateGraph` with a minimal state structure:
- State flows: Entry → "agent" node → END
- Messages are accumulated in the state's `messages` list
- The `call_model` function handles LLM invocation

## Environment Setup

### Required Environment Variables

Copy `.env.example` to `.env` and set:
- `OPENAI_API_KEY`: Your OpenAI API key (required for GPT-4o access)

### Installation

```bash
# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

## Development Commands

### Run the API Server

```bash
# Development server with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production server (as defined in main.py)
python main.py
```

### Test the API

```bash
# Using curl
curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d "{\"message\": \"Hello, agent!\"}"

# Using PowerShell Invoke-RestMethod
$body = @{ message = "Hello, agent!" } | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:8000/chat" -Method Post -Body $body -ContentType "application/json"
```

### API Documentation

Once running, access interactive API docs at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Extending the Agent

### Adding New Nodes

To add complexity to the agent workflow:
1. Define new node functions in `agent.py` that accept and return `AgentState`
2. Add nodes to the workflow: `workflow.add_node("node_name", node_function)`
3. Define edges between nodes: `workflow.add_edge("from_node", "to_node")`
4. For conditional routing, use `workflow.add_conditional_edges()`

### Adding Tools

To give the agent access to tools/functions:
1. Define tool functions using LangChain's `@tool` decorator
2. Bind tools to the model: `model.bind_tools([tool1, tool2])`
3. Add a tool-calling node to handle tool execution
4. Update the workflow to route between agent and tool nodes

## Deployment

This application is designed to run on fly.io (per user's infrastructure rules). Use `flyctl` commands for deployment.
