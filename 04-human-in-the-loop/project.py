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

def human_review(state: DeployState):
    # This node won't actually run logic in this pattern, 
    # but serves as a placeholder or can handle the resume input.
    print("--- Human Review Node ---")
    return {}

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

# Interrupt BEFORE 'deploy' node
memory = MemorySaver()
graph = builder.compile(checkpointer=memory, interrupt_before=["deploy"])

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "deploy-1"}}
    
    print("1. Starting Deployment...")
    graph.invoke({"approved": False}, config=config)
    
    print("\n2. Graph Paused. Waiting for user...")
    user_input = input("Do you approve this deployment? (yes/no): ")
    
    if user_input.lower() == "yes":
        print("\n3. Resuming with Approval...")
        # We update the state to set approved=True
        graph.invoke(Command(resume={"approved": True}), config=config)
    else:
        print("\n3. Resuming with Rejection...")
        graph.invoke(Command(resume={"approved": False}), config=config)
