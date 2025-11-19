from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

llm = ChatOpenAI(model="gpt-4o")

def editor_node(state):
    print("--- Editor Working ---")
    messages = state["messages"]
    
    # Generate a draft based on the conversation
    response = llm.invoke(
        [SystemMessage(content="You are an Editor. Write a short summary draft based on the research provided.")] + 
        messages
    )
    
    return {
        "messages": [response],
        "draft": response.content,
        "status": "finished" # We will pause before this state is finalized due to interrupt
    }
