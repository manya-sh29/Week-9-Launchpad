# DAY 4 — Memory Systems (Short-Term, Long-Term, Vector Memory)

##  Overview
The memory system enables agents to **store, recall, and reuse past information**.  
It improves contextual understanding and allows intelligent responses based on previous interactions.

The system is composed of **three memory layers**:
- Short-Term Memory
- Long-Term Memory
- Vector Memory

---

## Memory Types and Responsibilities

### Short-Term Memory (Session Memory)
**Purpose:**
Stores context during the active session.

**Characteristics:**
- Temporary and session-scoped
- Maintains recent conversation turns
- Cleared once the session ends

**Use Case:**
- Follow-up questions
- Context continuity in conversations

---

###  Long-Term Memory (Persistent Storage)
**Purpose:**
Stores important information across sessions.

**Implementation:**
- SQLite database (`long_term.db`)

**Stored Data:**
- Summarized facts
- User preferences
- Key historical interactions

**Use Case:**
- Persistent knowledge retention
- Cross-session recall

---

### Vector Memory (Similarity-Based Recall)
**Purpose:**  
Enables semantic search over stored memories.

**Implementation:**
- FAISS vector database

**Stored Data:**
- Embeddings of summarized memories
- Semantic representations of conversations

**Use Case:**
- Finding relevant past context
- Semantic similarity search

---

## Episodic vs Semantic Memory

| Memory Type | Description |
|------------|------------|
| Episodic | Stores specific events or interactions |
| Semantic | Stores generalized knowledge and facts |

---
