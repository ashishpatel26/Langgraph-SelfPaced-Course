# Module 02: State Management

## 🎯 Goal
Master the `State`. Learn how to define complex schemas, use **Reducers**, and manage data flow.

## 🧠 Concepts

### 1. `TypedDict` vs Pydantic
You can use either `TypedDict` or Pydantic models for your state. `TypedDict` is simpler for most cases.

### 2. Reducers (`Annotated`)
By default, when a node returns `{"key": "value"}`, it **overwrites** the existing value in the state.
Sometimes you want to **append** instead (like a list of messages).

```python
from typing import Annotated
from langgraph.graph.message import add_messages

class State(TypedDict):
    # This will APPEND new messages to the list, not overwrite
    messages: Annotated[list, add_messages] 
    total: int # This will OVERWRITE
```

### 3. Schema Validation
You can use the state to enforce structure. If a node tries to return a key that isn't in the state, it might be ignored or cause issues depending on configuration.

## 🏗️ Mini-Project: Order Processing Bot
We will build a bot that processes an order:
1.  **Validate**: Check if the items are in stock.
2.  **Calculate**: Sum up the prices.
3.  **Receipt**: Generate a final summary.
