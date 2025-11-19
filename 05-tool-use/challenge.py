from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

@tool
def search_flights(destination: str):
    """Search for flights to a destination."""
    print(f"--- Tool: Searching flights to {destination} ---")
    if "paris" in destination.lower():
        return "Flight 101: $500"
    return "No flights found."

# TODO: Define a weather tool
@tool
def get_weather(city: str):
    """Get the weather for a city."""
    # Return "Sunny" if city is Paris, else "Cloudy"
    pass

# TODO: Add the new tool to this list
tools = [search_flights]

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
    # The agent should now look up BOTH flights and weather
    print("User: Plan a trip to Paris. Check flights and weather.")
    result = graph.invoke({"messages": [("user", "Plan a trip to Paris. Check flights and weather.")]})
    print("\nFinal Answer:")
    print(result["messages"][-1].content)
