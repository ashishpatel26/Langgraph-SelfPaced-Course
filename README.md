# LangGraph Self-Paced Learning

Welcome to the **LangGraph Self-Paced Learning** repository! 🚀

This course is designed to take you from the basics of graph-based agents to building complex, production-ready multi-agent systems using **LangGraph 1.0**.

## 📚 Curriculum

The course is divided into 8 project-based modules:

1.  **[01-foundations](./01-foundations)**: "The Basics" - Build a Chain of Thought simulator.
2.  **[02-state-management](./02-state-management)**: "Order Processing System" - Build an order validation bot.
3.  **[03-persistence](./03-persistence)**: "Customer Support Bot" - Build a bot with memory.
4.  **[04-human-in-the-loop](./04-human-in-the-loop)**: "Deployment Manager" - Build a system that asks for approval.
5.  **[05-tool-use](./05-tool-use)**: "Travel Planner Agent" - Build an agent that uses tools.
6.  **[06-mcp-integration](./06-mcp-integration)**: "The Database Analyst" - Connect to external data via MCP.
7.  **[07-multi-agent-orchestration](./07-multi-agent-orchestration)**: "Software Dev Team" - Orchestrate a Supervisor, Coder, and Tester.
8.  **[08-capstone-project](./08-capstone-project)**: "Autonomous Research Assistant" - The final boss.

## 🛠️ Setup

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd Langgraph-latest
    ```

2.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up API Keys**:
    Copy `.env.example` to `.env` and fill in your keys:
    ```bash
    cp .env.example .env
    ```

## 🧠 How to Learn

Each module follows a **"Learn by Doing"** structure:

1.  **Read `concept.md`**: Understand the theory.
2.  **Run `project.py`**: See the working example.
3.  **Solve `challenge.py`**: Complete the missing code to finish the mini-project.
4.  **Check `solution.py`**: Verify your answer.

Happy coding! 🤖
