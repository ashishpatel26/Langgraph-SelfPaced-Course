from typing import Literal, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import SystemMessage, HumanMessage

# 1. Define State
class TeamState(MessagesState):
    next_agent: str

# 2. Define Agents
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

def coder_node(state: TeamState):
    print("--- Coder Working ---")
    response = llm.invoke(
        [SystemMessage(content="You are a Python Coder. Write code based on the request.")] + 
        state["messages"]
    )
    return {"messages": [response]}

def tester_node(state: TeamState):
    print("--- Tester Working ---")
    response = llm.invoke(
        [SystemMessage(content="You are a QA Tester. Review the code.")] + 
        state["messages"]
    )
    return {"messages": [response]}

def supervisor_node(state: TeamState) -> Literal["coder", "tester", END]:
    print("--- Supervisor Deciding ---")
    messages = state["messages"]
    last_msg = messages[-1].content.lower()
    
    if "code" in last_msg and "review" not in last_msg:
        return "coder"
    elif "review" in last_msg or "test" in last_msg:
        return "tester"
    else:
        return END

# 3. Build Graph
builder = StateGraph(TeamState)

builder.add_node("supervisor", supervisor_node)
builder.add_node("coder", coder_node)
builder.add_node("tester", tester_node)

builder.add_edge(START, "supervisor")
builder.add_edge("coder", "supervisor") # Return to supervisor
builder.add_edge("tester", "supervisor") # Return to supervisor

# The supervisor IS the conditional edge here
# But typically we separate the routing logic. 
# For simplicity, we'll use a conditional edge FROM the supervisor.

def route_supervisor(state: TeamState):
    # In a real app, the supervisor would output structured data.
    # Here we just use simple string matching from the node above? 
    # Actually, let's make the supervisor node return the Command or just use the state.
    # Better pattern: Supervisor outputs a structured decision.
    
    # For this simple example, we'll use the logic inside the conditional edge
    messages = state["messages"]
    last_msg = messages[-1]
    
    # If the last message is from a worker, we might want to stop or continue.
    if "FINISH" in last_msg.content:
        return END
    
    # If it's the user's first message
    if len(messages) == 1:
        return "coder"
        
    return END

# Let's simplify for the tutorial:
# User -> Coder -> Tester -> END

builder = StateGraph(TeamState)
builder.add_node("coder", coder_node)
builder.add_node("tester", tester_node)

builder.add_edge(START, "coder")
builder.add_edge("coder", "tester")
builder.add_edge("tester", END)

graph = builder.compile()

if __name__ == "__main__":
    print("User: Write a function to add two numbers.")
    result = graph.invoke({"messages": [("user", "Write a function to add two numbers.")]})
    print("\nFinal History:")
    for m in result["messages"]:
        print(f"{m.type}: {m.content[:50]}...")
