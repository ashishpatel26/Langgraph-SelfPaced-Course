from typing import Literal, TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_core.messages import SystemMessage

class TeamState(MessagesState):
    pass

llm = ChatOpenAI(model="gpt-4o")

def coder_node(state: TeamState):
    print("--- Coder Working ---")
    # TODO: If the previous message was from the Tester saying "FAIL", fix the code.
    response = llm.invoke(
        [SystemMessage(content="You are a Python Coder. Write code.")] + state["messages"]
    )
    return {"messages": [response]}

def tester_node(state: TeamState):
    print("--- Tester Working ---")
    # TODO: Simulate a test failure. 
    # If the code contains "bug", return "FAIL: Bug found".
    # Otherwise return "PASS".
    response = llm.invoke(
        [SystemMessage(content="You are a QA Tester. If you see 'bug', say FAIL. Else say PASS.")] + 
        state["messages"]
    )
    return {"messages": [response]}

# TODO: Implement a router that checks the Tester's output.
def router(state: TeamState):
    messages = state["messages"]
    last_msg = messages[-1].content
    
    if "FAIL" in last_msg:
        return "coder" # Loop back!
    return END

builder = StateGraph(TeamState)
builder.add_node("coder", coder_node)
builder.add_node("tester", tester_node)

builder.add_edge(START, "coder")
builder.add_edge("coder", "tester")

# TODO: Replace this with a conditional edge
# builder.add_edge("tester", END)
builder.add_conditional_edges("tester", router)

graph = builder.compile()

if __name__ == "__main__":
    # We force a bug to test the loop
    print("User: Write a python script with a bug in it.")
    result = graph.invoke({"messages": [("user", "Write a python script with a bug in it.")]})
    print("\nFinal History:")
    for m in result["messages"]:
        print(f"{m.type}: {m.content}")
