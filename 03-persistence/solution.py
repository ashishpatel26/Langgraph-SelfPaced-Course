from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages

class SupportState(TypedDict):
    messages: Annotated[list, add_messages]

def bot_node(state: SupportState):
    messages = state["messages"]
    last_user_msg = messages[-1].content.lower()
    
    if "summarize" in last_user_msg:
        summary = "Here is a summary of our chat:\n"
        for msg in messages[:-1]: # Exclude the 'summarize' request itself
            summary += f"- {msg.type}: {msg.content}\n"
        return {"messages": [summary]}
    
    if "name" not in last_user_msg and len(messages) < 2:
        return {"messages": ["Hi! I'm SupportBot. What is your name?"]}
    elif "issue" not in last_user_msg and len(messages) < 4:
        return {"messages": [f"Nice to meet you. What is your issue today?"]}
    else:
        return {"messages": ["Thanks, I've logged your ticket."]}

builder = StateGraph(SupportState)
builder.add_node("bot", bot_node)
builder.add_edge(START, "bot")
builder.add_edge("bot", END)

memory = MemorySaver()
graph = builder.compile(checkpointer=memory)

if __name__ == "__main__":
    config = {"configurable": {"thread_id": "user_2"}}
    
    # Pre-populate some conversation
    graph.invoke({"messages": [("user", "Hi")]}, config=config)
    graph.invoke({"messages": [("user", "My name is Bob")]}, config=config)
    graph.invoke({"messages": [("user", "My printer is on fire")]}, config=config)
    
    print("--- Testing Summary ---")
    print("User: summarize")
    result = graph.invoke({"messages": [("user", "summarize")]}, config=config)
    print("Bot:", result["messages"][-1].content)
