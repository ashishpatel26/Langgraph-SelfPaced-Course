from typing import TypedDict
from langgraph.graph import StateGraph, START, END

INVENTORY = {"apple": 1.0, "banana": 0.5, "orange": 1.2}

class OrderState(TypedDict):
    items: list[str]
    valid_items: list[str]
    total: float
    status: str

def validate_order(state: OrderState):
    print("--- Validating Order ---")
    valid = [item for item in state["items"] if item in INVENTORY]
    return {"valid_items": valid}

def calculate_total(state: OrderState):
    print("--- Calculating Total ---")
    total = sum(INVENTORY[item] for item in state["valid_items"])
    return {"total": total}

# TODO: Implement this node
def apply_discount(state: OrderState):
    print("--- Checking Discount ---")
    # If total > 2.0, apply 20% discount
    # Return updated total
    pass

def generate_receipt(state: OrderState):
    print("--- Generating Receipt ---")
    receipt = f"Receipt: {len(state['valid_items'])} items. Total: ${state['total']:.2f}"
    return {"status": receipt}

builder = StateGraph(OrderState)

builder.add_node("validator", validate_order)
builder.add_node("calculator", calculate_total)
# TODO: Add the discount node
# builder.add_node("discounter", apply_discount)
builder.add_node("receipt_printer", generate_receipt)

builder.add_edge(START, "validator")
builder.add_edge("validator", "calculator")
# TODO: Route calculator -> discounter -> receipt_printer
builder.add_edge("calculator", "receipt_printer")
builder.add_edge("receipt_printer", END)

graph = builder.compile()

if __name__ == "__main__":
    # This order should trigger a discount (Total 2.5)
    order = {"items": ["apple", "apple", "banana"], "valid_items": [], "total": 0.0, "status": ""}
    print("Processing Order...")
    result = graph.invoke(order)
    print("\nFinal State:", result)
