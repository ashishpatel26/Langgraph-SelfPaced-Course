from typing import TypedDict
import random
from langgraph.graph import StateGraph, START, END

# GOAL: Modify this graph to include a "Review" step.
# If the conclusion is "Weak", it should go back to "Analyze".
# If the conclusion is "Strong", it should go to END.

class ThinkingState(TypedDict):
    topic: str
    thoughts: list[str]
    conclusion: str
    quality: str  # "Strong" or "Weak"

def plan_step(state: ThinkingState):
    print("--- Step 1: Planning ---")
    return {"thoughts": ["Planning the approach"]}

def analyze_step(state: ThinkingState):
    print("--- Step 2: Analyzing ---")
    return {"thoughts": ["Crunching numbers"]}

def conclude_step(state: ThinkingState):
    print("--- Step 3: Concluding ---")
    # Simulate a random quality check
    quality = random.choice(["Strong", "Weak"])
    print(f"Conclusion Quality: {quality}")
    return {"conclusion": "Here is the result", "quality": quality}

# TODO: Define a conditional function
def check_quality(state: ThinkingState):
    # Return the name of the next node
    pass

builder = StateGraph(ThinkingState)

builder.add_node("planner", plan_step)
builder.add_node("analyst", analyze_step)
builder.add_node("concluder", conclude_step)

builder.add_edge(START, "planner")
builder.add_edge("planner", "analyst")
builder.add_edge("analyst", "concluder")

# TODO: Replace this normal edge with a conditional edge
# builder.add_edge("concluder", END)
# builder.add_conditional_edges("concluder", check_quality, {...})

graph = builder.compile()

if __name__ == "__main__":
    print("Running Challenge...")
    result = graph.invoke({"topic": "Quantum Physics", "thoughts": [], "conclusion": "", "quality": ""})
    print(result)
