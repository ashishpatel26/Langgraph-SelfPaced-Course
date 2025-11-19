from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END

# Mock Database
INVENTORY = {
    "apple": 1.0,
    "banana": 0.5,
    "orange": 1.2
}

# 1. Define State
class OrderState(TypedDict):
    items: list[str]
    valid_items: list[str]
    total: float
    status: str

# 2. Nodes
def validate_order(state: OrderState):
    print("--- Validating Order ---")
    valid = []
    for item in state["items"]:
        if item in INVENTORY:
            valid.append(item)
        else:
            print(f"Warning: {item} not in stock.")
    return {"valid_items": valid}

def calculate_total(state: OrderState):
    print("--- Calculating Total ---")
    total = sum(INVENTORY[item] for item in state["valid_items"])
    return {"total": total}

def generate_receipt(state: OrderState):
    print("--- Generating Receipt ---")
    receipt = f"Receipt: {len(state['valid_items'])} items. Total: ${state['total']:.2f}"
    return {"status": receipt}

# 3. Graph
builder = StateGraph(OrderState)

builder.add_node("validator", validate_order)
builder.add_node("calculator", calculate_total)
builder.add_node("receipt_printer", generate_receipt)

builder.add_edge(START, "validator")
builder.add_edge("validator", "calculator")
builder.add_edge("calculator", "receipt_printer")
builder.add_edge("receipt_printer", END)

graph = builder.compile()

if __name__ == "__main__":
    order = {"items": ["apple", "banana", "unicorn"], "valid_items": [], "total": 0.0, "status": ""}
    result = graph.invoke(order)
    print("\nFinal State:", result)
