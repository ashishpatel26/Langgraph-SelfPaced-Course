# Module 01: Foundations of LangGraph

## 🎯 Goal
Understand the core building blocks of LangGraph: **Nodes**, **Edges**, and the **StateGraph**.

## 🧠 Concepts

### 1. The State (`State`)
Every graph has a "State". Think of it as a shared dictionary that is passed around between nodes.
- When a node runs, it receives the current state.
- When a node finishes, it returns an update to the state.

### 2. Nodes (`add_node`)
Nodes are just Python functions. They do the work.
```python
def my_node(state: State):
    print("Doing work...")
    return {"key": "new value"}
```

### 3. Edges (`add_edge`)
Edges define the flow.
- **Normal Edge**: Go from Node A -> Node B.
- **Conditional Edge**: Go from Node A -> Node B OR Node C, depending on the result.

### 4. The Graph (`StateGraph`)
The graph orchestrates everything. You compile it into a `CompiledGraph` (a "Runnable") that you can invoke.

## 🏗️ Mini-Project: Chain of Thought Simulator
We will build a simple graph that simulates a thinking process:
1.  **Plan**: Decide what to do.
2.  **Analyze**: Think about the problem.
3.  **Conclude**: Give a final answer.
