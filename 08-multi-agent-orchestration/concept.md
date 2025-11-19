# Module 07: Multi-Agent Orchestration

## 🎯 Goal
Learn how to coordinate multiple agents to work together using the **Supervisor Pattern**.

## 🧠 Concepts

### 1. Single Agent vs Multi-Agent
- **Single Agent**: One LLM with many tools. Good for simple tasks.
- **Multi-Agent**: Specialized agents (e.g., a "Coder" and a "Tester") that collaborate. Good for complex tasks where separation of concerns is needed.

### 2. The Supervisor Pattern
A "Supervisor" LLM decides which agent should act next.
1.  Supervisor looks at the state.
2.  Supervisor outputs a `Command` to route to "Coder" or "Tester".
3.  Worker performs task and returns to Supervisor.

### 3. Handoffs
Agents can also hand off work directly to each other (Network Pattern), but we will focus on the Supervisor pattern here as it's easier to reason about.

## 🏗️ Mini-Project: Software Dev Team
We will build a team:
1.  **Coder**: Writes code.
2.  **Tester**: Reviews code.
3.  **Supervisor**: Manages the workflow.
