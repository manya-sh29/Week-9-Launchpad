# Day 1 — Agent Foundations & Message-Based Communication

---

## Overview
This document presents the foundational concepts of AI agents and demonstrates a practical implementation of a multi-agent system using **AutoGen** and **llama.cpp**.  
The focus is on understanding agent architecture, role isolation, and message-based communication through a structured pipeline of agents.

---

## What Is an AI Agent?
An **AI agent** is an autonomous software component that:

- Perceives input via messages or context
- Reasons using a language model
- Acts by producing outputs or communicating with other agents

Agents are **goal-oriented**, **role-driven**, and **modular**.

---


## Model Used
model : qwen2-7b-instruct-q4_k_m.gguf


---


## Message Flow
```
┌──────────────┐
│     User     │
│  (Query)     │
└──────┬───────┘
       │
       ▼
┌────────────────────┐
│  Research Agent    │
│  • Collects facts  │
│  • No summarizing  │
└──────┬─────────────┘
       │
       ▼
┌────────────────────┐
│ Summarizer Agent   │
│ • Condenses info   │
│ • Keeps accuracy   │
└──────┬─────────────┘
       │
       ▼
┌────────────────────┐
│   Answer Agent     │
│ • Final response   │
│ • Clear & concise  │
└────────────────────┘
```
---
# Implemented Agents

## 1. Research Agent
**Purpose**
- Gather detailed, factual information
- Avoid summarization or answering

**Output**
- Raw research data

---

## 2. Summarizer Agent
**Purpose**
- Condense research into structured summaries
- Preserve factual accuracy
- Remove redundancy

**Output**
- summaries in points

---

## 3. Answer Agent
**Purpose**
- Convert summaries into a final user-facing response
- Maintain clarity and conciseness

**Output**
- Final readable answer

---
## Screenshot


![alt text](<Screenshot from 2026-01-20 19-17-26.png>)
