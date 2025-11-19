from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

class DeployState(TypedDict):
    version: str
    approved: bool
    status: str

def prepare_deploy(state: DeployState):
    print("--- Preparing Deployment ---")
    return {"version": "v1.0.0", "status": "pending"}

def run_deploy(state: DeployState):
    if state.get("approved"):
        print(f"--- 🚀 DEPLOYING {state['version']} ---")
        return {"status": "deployed"}
    else:
        print("--- ❌ DEPLOYMENT CANCELLED ---")
        return {"status": "cancelled"}

builder = StateGraph(DeployState)
builder.add_node("prepare", prepare_deploy)
builder.add_node("deploy", run_deploy)

builder.add_edge(START, "prepare")
builder.add_edge("prepare", "deploy")
builder.add_edge("deploy", END)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory, interrupt_before=["deploy"])

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "deploy-2"}}
    
    print("1. Starting Deployment...")
    graph.invoke({"approved": False}, config=config)
    
    snapshot = graph.get_state(config)
    print(f"Current Version: {snapshot.values['version']}")
    
    print("\n2. Graph Paused.")
    # Simulate user input for the solution
    print("User Input: change")
    print("New Version: v2.0.0")
    
    # Solution logic
    graph.invoke(
        Command(resume={"approved": True, "version": "v2.0.0"}), 
        config=config
    )
