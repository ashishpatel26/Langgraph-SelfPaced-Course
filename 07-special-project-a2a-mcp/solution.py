import os
import sqlite3
from typing import Literal
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode

# Setup DB
def setup_db():
    conn = sqlite3.connect("special_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, message TEXT)")
    cursor.execute("INSERT OR IGNORE INTO logs (id, message) VALUES (1, 'System started')")
    cursor.execute("INSERT OR IGNORE INTO logs (id, message) VALUES (2, 'Error: Disk full')")
    conn.commit()
    conn.close()

setup_db()

@tool
def read_logs():
    """[Reader Tool] Read the logs table."""
    conn = sqlite3.connect("special_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    logs = cursor.fetchall()
    conn.close()
    return str(logs)

@tool
def write_alert(message: str):
    """[Writer Tool] Write an alert to a file."""
    print(f"!!! WRITING ALERT: {message} !!!")
    return "Alert written."

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found")

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key.strip())

reader_tools = [read_logs]
reader_llm = llm.bind_tools(reader_tools)

writer_tools = [write_alert]
writer_llm = llm.bind_tools(writer_tools)

def reader_node(state: MessagesState):
    print("--- Reader Working ---")
    return {"messages": [reader_llm.invoke(state["messages"])]}

def writer_node(state: MessagesState):
    print("--- Writer Working ---")
    return {"messages": [writer_llm.invoke(state["messages"])]}

def route_reader(state: MessagesState) -> Literal["reader_tools", "writer", END]:
    messages = state["messages"]
    last_msg = messages[-1]
    
    if last_msg.tool_calls:
        return "reader_tools"
    
    if "Error" in last_msg.content:
        print("--- Handoff: Reader -> Writer ---")
        return "writer"
        
    return END

def route_writer(state: MessagesState) -> Literal["writer_tools", END]:
    messages = state["messages"]
    last_msg = messages[-1]
    
    if last_msg.tool_calls:
        return "writer_tools"
        
    return END

builder = StateGraph(MessagesState)

builder.add_node("reader", reader_node)
builder.add_node("reader_tools", ToolNode(reader_tools))
builder.add_node("writer", writer_node)
builder.add_node("writer_tools", ToolNode(writer_tools))

builder.add_edge(START, "reader")
builder.add_conditional_edges("reader", route_reader)
builder.add_edge("reader_tools", "reader")

builder.add_conditional_edges("writer", route_writer)
builder.add_edge("writer_tools", "writer")

graph = builder.compile()

if __name__ == "__main__":
    print("User: Check logs for errors and alert if found.")
    result = graph.invoke({"messages": [("user", "Check logs for errors and alert if found.")]})
    print("\nFinal Answer:")
    print(result["messages"][-1].content)
