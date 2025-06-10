# main.py
import asyncio
from langgraph.graph import StateGraph, END
from state import ForgeState
from agents.planner_agent import PlannerAgent

async def main():
    """
    This is the main function that sets up and runs our agentic workflow.
    """
    print("DEBUG: Entered the main() function.")
    
    # SETUP: For this test run, we need a file for our agent to read.
    with open("prompt.txt", "w", encoding="utf-8") as f:
        f.write("This is the initial task from the user.")
    print("DEBUG: Created a dummy 'prompt.txt' file for the test.")

    # 1. Initialize our agent
    planner_agent = PlannerAgent()
    print("DEBUG: Initialized PlannerAgent.")

    # 2. Define the graph
    workflow = StateGraph(ForgeState)
    workflow.add_node("planner", planner_agent.run)
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", END)
    print("DEBUG: Graph definition complete.")

    # 3. Compile the graph
    app = workflow.compile()
    print("DEBUG: Workflow compiled successfully.")

    print("\n--- Running The Forge ---")
    initial_state = {"task": "prompt.txt"}
    
    # 4. Invoke the graph inside a try/except block to catch any errors
    final_state = None
    try:
        print("DEBUG: About to invoke the graph...")
        final_state = await app.ainvoke(initial_state)
        print("DEBUG: Graph invocation finished.")
    except Exception as e:
        print(f"FATAL ERROR during graph invocation: {e}")
        import traceback
        traceback.print_exc() # Print the full error stack trace

    print("\n--- The Forge has finished its run ---")
    print("Final State:")
    print(final_state)

if __name__ == "__main__":
    # This block is what runs when you execute 'python main.py'
    print("DEBUG: Script started. Running main function...")
    asyncio.run(main())
    print("DEBUG: Script finished.")