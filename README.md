# Assignment 2 — Part 2: Structured Output Agent

An upgraded Python-based AI agent built on top of Part 1, featuring structured tool calling, file editing, persistent session history, output size limits, and Docker-based sandboxed execution. The agent is designed to work safely and reliably as part of a larger multi-agent software development organization.

## Table of Contents

- [Overview](#overview)
- [What's New in Part 2](#whats-new-in-part-2)
- [How It Works](#how-it-works)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Configuration](#configuration)
- [Running with Docker](#running-with-docker)
- [Security](#security)
- [Constraints](#constraints)

## Overview

Part 2 builds on the ReAct agent from Part 1 by replacing the raw text parser with structured output, adding new tools, and wrapping the entire agent in a Docker container for safe execution. The agent uses the OpenAI API (GPT-4o) as its language model, and all core logic — the agent loop, tool dispatch, context management, and safety controls — is written from scratch in Python.

## What's New in Part 2

- **Structured output** — the model returns validated JSON tool calls instead of raw text, replacing the hand-built string parser from Part 1
- **File editing** — the agent can edit specific sections of files without rewriting the entire file
- **Multi-round tool calling** — the model decides autonomously how many tool calls to make before yielding a final answer to the user
- **Persistent session history** — the full conversation is kept in memory throughout the session so the agent maintains context across multiple exchanges
- **System prompt from config file** — the agent's behavior is defined in a separate config file, scoping it to software engineering tasks only
- **Tool output size limit** — responses from tools are truncated at a configurable limit, and the agent is aware of this constraint
- **Docker sandboxing** — the agent runs inside an isolated container, protecting the host machine from unintended or destructive commands

## How It Works

```
You give a task
      │
      ▼
Model reasons and returns a structured tool call
{"tool": "bash", "command": "ls -la"}
      │
      ▼
Agent loop dispatches to the correct tool
      │
      ▼
Tool output is captured and truncated if needed
      │
      ▼
Output is added to session history
      │
      ▼
Model decides: another tool call or Final Answer?
      │
      ▼
Loop continues until model yields to the user
```

## Project Structure

```
part-2/
├── agent.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env                 
├── .gitignore
├── config/
│   └── system_prompt.md
├── src/
│   ├── agent_loop.py
│   ├── llm_client.py
│   ├── session.py
│   ├── safety.py
│   ├── output_limiter.py
│   ├── tool_registry.py
│   └── tools/
│       ├── bash_tool.py
│       └── file_editor.py
└── logs/
```

## Requirements

- Python 3.10 
- Docker Desktop
- OpenAI API key (platform.openai.com)

## Configuration

Create a `.env` file in the project root:

```env
BASE_URL=https://api.openai.com/v1
MODEL=gpt-4o
API_KEY=your-openai-api-key-here
TOOL_OUTPUT_LIMIT=4000
```

The agent's behavior is defined in `config/system_prompt.md`. This file instructs the agent to only handle software engineering tasks, decline unrelated topics, and not leak sensitive information.

## Running with Docker

Build and start the container:

```bash
docker compose up --build
```

The agent runs fully inside the container. Any bash commands executed by the agent affect only the container environment, not your local machine.

To stop the container:

```bash
docker compose down
```

## Security

- **Docker isolation** — the agent runs in a sandboxed container, protecting the host machine
- **Command filtering** — a safety layer blocks destructive bash commands before execution
- **Output size limits** — tool responses are truncated to prevent oversized context and unexpected API costs
- **Session token budget** — a maximum token limit per session prevents runaway API usage
- **Config-based system prompt** — the agent is scoped to software engineering only and will decline other topics
- **No secrets in version control** — the `.env` file is excluded via `.gitignore` and never pushed to GitHub

## Constraints

- Built entirely in Python with direct calls to the OpenAI API
- No pre-built agent products used (Cursor, Claude Code, Codex, etc.)
- Structured output is used for tool calling, but the agent loop, context handling, and tool dispatch are all custom code
- No agent frameworks (LangChain, LangGraph, etc.)
- All core components written from scratch