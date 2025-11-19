# Module 04: Human-in-the-Loop (HITL)

## 🎯 Goal
Learn how to **pause** your agent to get user feedback, approval, or input before proceeding.

## 🧠 Concepts

### 1. Interrupts (`interrupt_before`)
You can tell the graph to stop *before* executing a specific node.
```python
graph = builder.compile(checkpointer=memory, interrupt_before=["deploy_node"])
```
When the graph hits `deploy_node`, it will stop and save state.

### 2. Resuming (`Command`)
To resume, you call `graph.invoke` again with a `Command`.
- **Simple Resume**: Just continue.
- **Update State**: Change something in the state before continuing.

```python
from langgraph.types import Command
# Resume and update the "approved" flag
graph.invoke(Command(resume={"approved": True}), config=config)
```

## 🏗️ Mini-Project: Deployment Manager
We will build a workflow that:
1.  **Prepares** a deployment (generates a version number).
2.  **Pauses** for human approval.
3.  **Deploys** only if approved.
