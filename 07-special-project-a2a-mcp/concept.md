# Special Project: A2A + MCP (The Data Pipeline)

## 🎯 Goal
Combine **Agent-to-Agent (A2A)** communication with **MCP** to build a robust data pipeline.

## 🧠 Concepts

### 1. The Network Pattern (A2A)
Unlike the Supervisor pattern where a central node decides everything, in the **Network Pattern**, agents talk directly to each other.
- Agent A does work -> Handoff to Agent B.
- Agent B does work -> Handoff to Agent C or END.

### 2. Distributed MCP Tools
We can split our tools across different agents to enforce "Separation of Concerns".
- **Scout Agent**: Has `list_tables` (Can see *what* exists, but can't read data).
- **Analyst Agent**: Has `run_query` (Can read data, but needs to know the table name).

This forces the agents to collaborate! The Scout must find the table and tell the Analyst "Hey, query table X".

## 🏗️ Project: The Data Pipeline
1.  **Scout**: Connects to DB, finds the "users" table.
2.  **Handoff**: Passes the table name to Analyst.
3.  **Analyst**: Queries the table and summarizes the data.
