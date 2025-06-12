import asyncio
from langgraph.graph import StateGraph, END
from state import ForgeState
from agents.planner_agent import PlannerAgent
from agents.code_generator_agent import CodeGenerationAgent

# 1. Initialize our agents
planner_agent = PlannerAgent()
coder_agent = CodeGenerationAgent()

# 2. Define the graph nodes
workflow = StateGraph(ForgeState)
workflow.add_node("planner", planner_agent.run)
workflow.add_node("coder", coder_agent.execute_step)

# 3. Define the routing logic function
def should_continue(state: ForgeState):
    """
    This is our "router." It checks the state and decides where to go next.
    """
    print("---ROUTER: Checking state...---")
    # If there was an error in the last step, end the workflow.
    if state.get("error"):
        print("---ROUTER: Error detected. Ending workflow.---")
        return "end"

    # Get the plan and the current step from the state.
    plan = state.get("plan", [])
    current_step = state.get("current_step", 0)

    # If the current step is beyond the length of the plan, we're done.
    if current_step >= len(plan):
        print("---ROUTER: Plan complete. Ending workflow.---")
        return "end"
    else:
        # Otherwise, continue to the coder.
        print(f"---ROUTER: Plan has {len(plan) - current_step} steps remaining. Continuing.---")
        return "continue_coding"

# 4. Wire up the graph with edges
workflow.set_entry_point("planner")

# After the planner runs, the first step always goes to the coder.
workflow.add_edge("planner", "coder")

# After the coder runs a step, we go to our "should_continue" router.
# The router will then decide whether to loop back to the 'coder' node
# or go to the special 'END' node.
workflow.add_conditional_edges(
    "coder",
    should_continue,
    {
        "continue_coding": "coder", # If the router returns this, loop back.
        "end": END                 # If the router returns this, finish.
    }
)

# 5. Compile the graph into a runnable application
app = workflow.compile()
print("--- The Forge workflow is compiled and ready. ---")

# This part allows us to run the test from the command line.
async def run_the_forge():
    print("\n--- Starting a new run of The Forge ---")
    task = "Create a simple python script named 'hello.py' that prints 'hello from The Forge'."
    initial_state: ForgeState = {"task": task}

    # Stream the events to see the flow in real-time
    async for event in app.astream(initial_state):
        for key, value in event.items():
            print(f"--- Event: Node '{key}' ---")
            print(value)
            print("\n")

if __name__ == "__main__":
    asyncio.run(run_the_forge())