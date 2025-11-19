from typing import Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

# 1. Define Tools
@tool
def search_flights(destination: str):
    """Search for flights to a destination."""
    print(f"--- Tool: Searching flights to {destination} ---")
    if "paris" in destination.lower():
        return "Flight 101: $500"
    return "No flights found."

tools = [search_flights]

# 2. Define Agent
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
llm_with_tools = llm.bind_tools(tools)

def agent_node(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# 3. Build Graph
builder = StateGraph(MessagesState)

builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "agent")
# Prebuilt conditional edge that checks if the LLM requested a tool
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

graph = builder.compile()

if __name__ == "__main__":
    print("User: I want to go to Paris")
    result = graph.invoke({"messages": [("user", "I want to go to Paris")]})
    print("\nFinal Answer:")
    print(result["messages"][-1].content)
