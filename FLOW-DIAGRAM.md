# Day 2 — Multi-Agent Orchestration

## Overview

* This document presents the 4-Agent Architecture for Day 2, based on a Planner → Workers → Reflection → Validator chain-of-command.
* The system demonstrates how a user query is decomposed into smaller tasks and executed using parallel worker agents.
* A reflection agent refines the combined output, while a validator ensures correctness and reliability.
This architecture models real-world multi-agent orchestration using task planning, DAG-based execution, and validation.

---

## Agent Roles

### 1. Orchestrator / Planner

* Entry point of the system
* Receives the user query
* Breaks the query into smaller tasks
* Builds a task graph (DAG)
* Assigns tasks to Worker Agents

### 2. Worker Agent(s)

* Execute individual tasks assigned by the Orchestrator
* Can run **in parallel**

### 3. Reflection Agent

* Reviews combined worker outputs
* Improves clarity, correctness, and structure
* Removes redundancy

### 4. Validator Agent

* Verifies final response
* Checks for logical, factual, or formatting errors
* Approves or flags issues before output

---

## Execution Flow

```text
User Query
    ↓
Orchestrator / Planner
    ↓
Parallel Worker Agents
    ↓
Reflection Agent
    ↓
Validator Agent
    ↓
Final Answer
```

---

## DAG-Based Task Execution

Each task created by the Orchestrator forms a **Directed Acyclic Graph (DAG)**.

* Nodes represent tasks
* Edges represent dependencies
* Independent tasks are executed in parallel

### Example DAG

```text
          User Query
               |
        -----------------
        |       |       |
     Task A  Task B  Task C   (Parallel Workers)
        \       |       /
         --------|------
                  ↓
           Reflection Task
                  ↓
            Validation Task
```

---

## Execution Tree Representation

```text
Orchestrator
├── Worker Agent 1: Task A
├── Worker Agent 2: Task B
├── Worker Agent 3: Task C
│
└── Reflection Agent
     └── Validator Agent
```

---

## Deliverables Mapping

| File Path                  | Responsibility                              |
| -------------------------- | ------------------------------------------- |
| `/orchestrator/planner.py` | Task planning, DAG creation, delegation     |
| `/agents/worker_agent.py`  | Task execution (parallel workers)           |
| `/agents/validator.py`     | Final validation logic                      |
| `FLOW-DIAGRAM.md`          | Architecture & execution flow documentation |

---

