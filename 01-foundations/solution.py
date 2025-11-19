from typing import TypedDict, Literal
import random
from langgraph.graph import StateGraph, START, END

class ThinkingState(TypedDict):
    topic: str
    thoughts: list[str]
    conclusion: str
    quality: str

def plan_step(state: ThinkingState):
    print("--- Step 1: Planning ---")
    return {"thoughts": ["Planning the approach"]}

def analyze_step(state: ThinkingState):
    print("--- Step 2: Analyzing ---")
    return {"thoughts": ["Crunching numbers"]}

def conclude_step(state: ThinkingState):
    print("--- Step 3: Concluding ---")
    # For demonstration, we alternate or randomize. 
    # Let's make it random but biased so it eventually finishes.
    quality = random.choice(["Strong", "Weak", "Strong"]) 
    print(f"Conclusion Quality: {quality}")
    return {"conclusion": "Here is the result", "quality": quality}

def check_quality(state: ThinkingState) -> Literal["analyst", END]:
    if state["quality"] == "Weak":
        print("!!! Quality is Weak, going back to Analysis !!!")
        return "analyst"
    return END

builder = StateGraph(ThinkingState)

builder.add_node("planner", plan_step)
builder.add_node("analyst", analyze_step)
builder.add_node("concluder", conclude_step)

builder.add_edge(START, "planner")
builder.add_edge("planner", "analyst")
builder.add_edge("analyst", "concluder")

# Conditional Edge
builder.add_conditional_edges(
    "concluder", 
    check_quality, 
    {"analyst": "analyst", END: END}
)

graph = builder.compile()

if __name__ == "__main__":
    print("Running Solution...")
    result = graph.invoke({"topic": "Quantum Physics", "thoughts": [], "conclusion": "", "quality": ""})
    print("\nFinal State:", result)
