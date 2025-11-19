from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from tools.search import mock_search

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

def researcher_node(state):
    print("--- Researcher Working ---")
    messages = state["messages"]
    
    # Simple logic: If we haven't searched yet, search.
    # If we have searched, say we are done.
    
    # Check if we have search results in history
    has_results = any("Search Results" in m.content for m in messages)
    
    if not has_results:
        query = messages[-1].content
        results = mock_search(query)
        return {
            "messages": [("assistant", f"Search Results: {results}")],
            "status": "drafting" # Move to drafting next
        }
    
    return {"status": "drafting"}
