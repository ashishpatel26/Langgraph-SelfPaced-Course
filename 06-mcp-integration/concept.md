# Module 06: Model Context Protocol (MCP)

## 🎯 Goal
Learn how to connect your agent to external data sources using the **Model Context Protocol (MCP)**.

## 🧠 Concepts

### 1. What is MCP?
MCP is a standard protocol that allows AI agents to connect to "Servers" (like Google Drive, Slack, or a Database) without writing custom integration code for each one.
- **MCP Server**: Exposes "Resources" (data) and "Tools" (actions).
- **MCP Client**: Your agent, which connects to the server to read data or perform actions.

### 2. Tools as MCP Clients
In LangGraph, we typically wrap an MCP client as a standard Python tool.
```python
@tool
def query_database(query: str):
    # Under the hood, this sends an MCP request to the server
    return mcp_client.call_tool("query", query)
```

## 🏗️ Mini-Project: The Database Analyst
We will build an agent that acts as a Data Analyst.
Instead of a real remote server (which requires complex setup), we will **simulate** an MCP connection to a local SQLite database.
1.  **Resources**: The agent can "read" the database schema.
2.  **Tools**: The agent can "run" SQL queries.
