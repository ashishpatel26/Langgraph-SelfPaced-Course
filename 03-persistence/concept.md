# Module 03: Persistence (Memory)

## 🎯 Goal
Learn how to give your graph "Memory" so it can remember past interactions, even if the script restarts.

## 🧠 Concepts

### 1. Checkpointers (`MemorySaver`)
A checkpointer saves the state of the graph at every step.
- `MemorySaver`: Saves to RAM (lost on restart).
- `SqliteSaver`: Saves to a SQLite database (persists on restart).

### 2. Thread IDs (`config`)
To distinguish between different users or conversations, we use a `thread_id`.
When you invoke the graph, you pass a config:
```python
config = {"configurable": {"thread_id": "user_123"}}
graph.invoke(input, config=config)
```
The graph looks up the state for "user_123" and resumes from there.

### 3. Time Travel
Because every step is saved, you can actually "rewind" the graph to a previous state (useful for debugging or human-in-the-loop), though we will cover that more in the next module.

## 🏗️ Mini-Project: Customer Support Bot
We will build a bot that:
1.  Asks for your name.
2.  Asks for your issue.
3.  Remembers both even if you run the script multiple times (simulated loop).
