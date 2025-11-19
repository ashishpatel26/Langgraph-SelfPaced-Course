from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages

# 1. State
class SupportState(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Nodes
def bot_node(state: SupportState):
    messages = state["messages"]
    last_user_msg = messages[-1].content
    
    # Simple logic to simulate a conversation
    if "name" not in last_user_msg.lower() and len(messages) < 2:
        return {"messages": ["Hi! I'm SupportBot. What is your name?"]}
    elif "issue" not in last_user_msg.lower() and len(messages) < 4:
        return {"messages": [f"Nice to meet you. What is your issue today?"]}
    else:
        return {"messages": ["Thanks, I've logged your ticket."]}

# 3. Graph
builder = StateGraph(SupportState)
builder.add_node("bot", bot_node)
builder.add_edge(START, "bot")
builder.add_edge("bot", END)

# 4. Compile with Checkpointer
memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

# 5. Run with Thread ID
if __name__ == "__main__":
    config = {"configurable": {"thread_id": "user_1"}}
    
    print("--- Conversation Start ---")
    
    # Turn 1
    print("User: Hi")
    graph.invoke({"messages": [("user", "Hi")]}, config=config)
    snapshot = graph.get_state(config)
    print("Bot:", snapshot.values["messages"][-1].content)
    
    # Turn 2
    print("\nUser: My name is Alice")
    graph.invoke({"messages": [("user", "My name is Alice")]}, config=config)
    snapshot = graph.get_state(config)
    print("Bot:", snapshot.values["messages"][-1].content)
    
    # Turn 3
    print("\nUser: I have a login issue")
    graph.invoke({"messages": [("user", "I have a login issue")]}, config=config)
    snapshot = graph.get_state(config)
    print("Bot:", snapshot.values["messages"][-1].content)
