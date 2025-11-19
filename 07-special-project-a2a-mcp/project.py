import sqlite3
from typing import Literal, TypedDict, Annotated
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph.message import add_messages

# Setup DB
def setup_db():
    conn = sqlite3.connect("special_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
    cursor.execute("INSERT OR IGNORE INTO products (id, name, price) VALUES (1, 'SuperWidget', 99.99)")
    cursor.execute("INSERT OR IGNORE INTO products (id, name, price) VALUES (2, 'MegaGadget', 149.50)")
    conn.commit()
    conn.close()

setup_db()

# --- MCP TOOLS ---

@tool
def list_tables():
    """[Scout Tool] List all tables in the database."""
    conn = sqlite3.connect("special_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return str(tables)

@tool
def run_query(query: str):
    """[Analyst Tool] Run a SQL query on the database."""
    conn = sqlite3.connect("special_db.sqlite")
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return str(result)
    except Exception as e:
        return f"Error: {e}"
    finally:
        conn.close()

# --- AGENTS ---

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

# Scout: Only has list_tables
scout_tools = [list_tables]
scout_llm = llm.bind_tools(scout_tools)

# Analyst: Only has run_query
analyst_tools = [run_query]
analyst_llm = llm.bind_tools(analyst_tools)

def scout_node(state: MessagesState):
    print("--- Scout Working ---")
    return {"messages": [scout_llm.invoke(state["messages"])]}

def analyst_node(state: MessagesState):
    print("--- Analyst Working ---")
    return {"messages": [analyst_llm.invoke(state["messages"])]}

# --- ROUTING LOGIC (A2A) ---

def route_scout(state: MessagesState) -> Literal["scout_tools", "analyst", END]:
    messages = state["messages"]
    last_msg = messages[-1]
    
    # If tool call, go to tools
    if last_msg.tool_calls:
        return "scout_tools"
    
    # If Scout found the table, handoff to Analyst
    if "products" in last_msg.content:
        print("--- Handoff: Scout -> Analyst ---")
        return "analyst"
        
    return END

def route_analyst(state: MessagesState) -> Literal["analyst_tools", END]:
    messages = state["messages"]
    last_msg = messages[-1]
    
    if last_msg.tool_calls:
        return "analyst_tools"
        
    return END

# --- GRAPH ---

builder = StateGraph(MessagesState)

builder.add_node("scout", scout_node)
builder.add_node("scout_tools", ToolNode(scout_tools))
builder.add_node("analyst", analyst_node)
builder.add_node("analyst_tools", ToolNode(analyst_tools))

builder.add_edge(START, "scout")
builder.add_conditional_edges("scout", route_scout)
builder.add_edge("scout_tools", "scout")

builder.add_conditional_edges("analyst", route_analyst)
builder.add_edge("analyst_tools", "analyst")

graph = builder.compile()

if __name__ == "__main__":
    print("User: Find the products table and tell me the price of SuperWidget.")
    # We give a hint to start
    result = graph.invoke({"messages": [("user", "Find the products table and tell me the price of SuperWidget.")]})
    print("\nFinal Answer:")
    print(result["messages"][-1].content)
