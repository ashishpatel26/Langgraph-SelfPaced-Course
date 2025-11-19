# Module 05: Tool Use (Agents)

## 🎯 Goal
Build a real "Agent" that can use tools (Python functions) to solve problems.

## 🧠 Concepts

### 1. `MessagesState`
LangGraph provides a pre-built state called `MessagesState` that is perfect for chat agents. It handles the list of messages automatically.

### 2. Binding Tools (`bind_tools`)
LLMs (like OpenAI) need to know what tools are available. We "bind" the tools to the model.
```python
tools = [my_tool]
llm_with_tools = llm.bind_tools(tools)
```

### 3. `ToolNode`
LangGraph provides a pre-built node called `ToolNode` that executes the tools requested by the LLM.

### 4. The ReAct Loop
The standard pattern is:
1.  **Agent Node**: LLM decides what to do.
2.  **Conditional Edge**:
    - If LLM wants to call a tool -> Go to `tools`.
    - If LLM is done -> Go to `END`.
3.  **Tool Node**: Execute tool and go back to **Agent Node**.

## 🏗️ Mini-Project: Travel Planner
We will build an agent that can:
1.  Search for flights (Mock tool).
2.  Search for weather (Challenge).
