import sqlite3
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

# Setup DB
def setup_db():
    conn = sqlite3.connect("test_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, user_id INTEGER, amount REAL)")
    cursor.execute("INSERT OR IGNORE INTO orders (id, user_id, amount) VALUES (101, 1, 50.0)")
    cursor.execute("INSERT OR IGNORE INTO orders (id, user_id, amount) VALUES (102, 2, 100.0)")
    conn.commit()
    conn.close()

setup_db()

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

# TODO: Create a new tool that simulates a "FileSystem" MCP server
# It should allow writing the final report to a file.
@tool
def write_report(filename: str, content: str):
    """Write a report to the local filesystem."""
    pass

# TODO: Add the new tool to the list
tools = [list_tables, run_query]

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
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
    # The agent should query the DB and then WRITE a report file
    print("User: Analyze the orders table and write a report to 'report.txt'.")
    result = graph.invoke({"messages": [("user", "Analyze the orders table and write a report to 'report.txt'.")]})
    print("\nFinal Answer:")
    print(result["messages"][-1].content)
