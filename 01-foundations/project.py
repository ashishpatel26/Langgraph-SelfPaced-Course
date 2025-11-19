from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Define the State
class ThinkingState(TypedDict):
    topic: str
    thoughts: list[str]
    conclusion: str

# 2. Define the Nodes
def plan_step(state: ThinkingState):
    print("--- Step 1: Planning ---")
    return {"thoughts": ["I need to research this topic."]}

def analyze_step(state: ThinkingState):
    print("--- Step 2: Analyzing ---")
    return {"thoughts": ["Analyzing the data...", "Looking for patterns..."]}

def conclude_step(state: ThinkingState):
    print("--- Step 3: Concluding ---")
    return {"conclusion": "The data suggests a positive trend."}

# 3. Build the Graph
builder = StateGraph(ThinkingState)

# Add nodes
builder.add_node("planner", plan_step)
builder.add_node("analyst", analyze_step)
builder.add_node("concluder", conclude_step)

# Add edges (Flow)
builder.add_edge(START, "planner")
builder.add_edge("planner", "analyst")
builder.add_edge("analyst", "concluder")
builder.add_edge("concluder", END)

# 4. Compile
graph = builder.compile()

# 5. Run
if __name__ == "__main__":
    initial_state = {"topic": "AI Agents", "thoughts": [], "conclusion": ""}
    result = graph.invoke(initial_state)
    
    print("\nFinal Result:")
    print(result)
