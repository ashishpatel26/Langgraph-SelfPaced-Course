from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

# Import our agents
from agents.researcher import researcher_node
from agents.editor import editor_node

class ResearchState(TypedDict):
    messages: Annotated[list, add_messages]
    status: str # "researching", "drafting", "reviewing", "finished"
    draft: str

def supervisor_node(state: ResearchState):
    status = state.get("status", "researching")
    
    if status == "researching":
        return "researcher"
    elif status == "drafting":
        return "editor" # Editor will also draft for simplicity
    elif status == "reviewing":
        # Pause for human review
        pass 
    return END

builder = StateGraph(ResearchState)

builder.add_node("researcher", researcher_node)
builder.add_node("editor", editor_node)

builder.add_edge(START, "researcher")

# Logic to route based on state
def route_workflow(state: ResearchState):
    status = state.get("status")
    if status == "researching":
        return "researcher"
    elif status == "drafting":
        return "editor"
    elif status == "finished":
        return END
    return END

builder.add_conditional_edges("researcher", route_workflow)
builder.add_conditional_edges("editor", route_workflow)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory, interrupt_before=["editor"])

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "capstone-1"}}
    
    print("--- Starting Research Assistant ---")
    initial_input = {"messages": [("user", "Research the history of the Internet.")], "status": "researching"}
    
    # Run until interrupted
    for event in graph.stream(initial_input, config=config):
        pass
    
    print("\n--- Paused for Review ---")
    snapshot = graph.get_state(config)
    print("Current Draft:", snapshot.values.get("draft", "No draft yet"))
    
    approve = input("Approve draft? (yes/no): ")
    if approve == "yes":
        graph.invoke(Command(resume={"status": "finished"}), config=config)
        print("--- Finished ---")
    else:
        print("--- Sending back to Researcher ---")
        graph.invoke(Command(resume={"status": "researching", "messages": [("user", "More research needed.")]}), config=config)
