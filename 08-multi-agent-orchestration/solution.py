from typing import Literal, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import SystemMessage

class TeamState(MessagesState):
    pass

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

def coder_node(state: TeamState):
    print("--- Coder Working ---")
    response = llm.invoke(
        [SystemMessage(content="You are a Python Coder. If asked to fix, fix the code.")] + 
        state["messages"]
    )
    return {"messages": [response]}

def tester_node(state: TeamState):
    print("--- Tester Working ---")
    # We instruct the LLM to be a harsh critic for demonstration
    response = llm.invoke(
        [SystemMessage(content="You are a QA Tester. If the code looks buggy or simple, say 'FAIL'. If it is perfect, say 'PASS'.")] + 
        state["messages"]
    )
    return {"messages": [response]}

def router(state: TeamState) -> Literal["coder", END]:
    messages = state["messages"]
    last_msg = messages[-1].content
    
    if "FAIL" in last_msg:
        print("!!! Tests Failed. Sending back to Coder !!!")
        return "coder"
    
    print("Tests Passed. Finishing.")
    return END

builder = StateGraph(TeamState)
builder.add_node("coder", coder_node)
builder.add_node("tester", tester_node)

builder.add_edge(START, "coder")
builder.add_edge("coder", "tester")
builder.add_conditional_edges("tester", router)

graph = builder.compile()

if __name__ == "__main__":
    # We ask for something that might trigger a fail first
    print("User: Write a function that divides by zero.")
    # We limit recursion to avoid infinite loops in this demo
    result = graph.invoke(
        {"messages": [("user", "Write a function that divides by zero.")]}, 
        {"recursion_limit": 10}
    )
    print("\nFinal History:")
    for m in result["messages"]:
        print(f"{m.type}: {m.content}")
