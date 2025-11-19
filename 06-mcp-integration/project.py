import sqlite3
from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

# Setup a dummy database
def setup_db():
    conn = sqlite3.connect("test_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (1, 'Alice', 'alice@example.com')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name, email) VALUES (2, 'Bob', 'bob@example.com')")
    conn.commit()
    conn.close()

setup_db()

# --- SIMULATED MCP TOOLS ---

@tool
def list_tables():
    """[MCP Resource] List all tables in the database."""
    conn = sqlite3.connect("test_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return str(tables)

@tool
def run_query(query: str):
    """[MCP Tool] Run a SQL query on the database."""
    # Security warning: Don't do this in prod without validation!
    conn = sqlite3.connect("test_db.sqlite")
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return str(result)
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()

tools = [list_tables, run_query]

# --- AGENT ---

llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)

def agent_node(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

if __name__ == "__main__":
    print("User: Who is in the users table?")
    result = graph.invoke({"messages": [("user", "Who is in the users table?")]})
    print("\nFinal Answer:")
    print(result["messages"][-1].content)
