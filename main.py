import asyncio
import os
import argparse
import shutil
from langgraph.graph import StateGraph, END
from state import ForgeState
from agents.planner_agent import PlannerAgent
from agents.code_generator_agent import CodeGenerationAgent
from agents.test_engineer_agent import TestEngineerAgent
from agents.debugger_agent import DebuggerAgent

RETRY_LIMIT = 5

def human_review_node(state: ForgeState):
    print("\n" + "="*40 + "\n--- HUMAN REVIEW REQUIRED ---\n" + "="*40)
    plan = state.get("plan")
    if not plan:
        print("No plan generated.")
        return {"error": "No plan generated."}
    
    print("The AI Planner has generated the following plan:")
    for i, step in enumerate(plan):
        print(f"  Step {i+1}: {step}")

    while True:
        user_input = input("\nDo you approve this plan? (y/n): ").lower().strip()
        if user_input == 'y':
            print("--- Plan approved. Proceeding. ---")
            return {"error": None}
        elif user_input == 'n':
            print("--- Plan rejected. Ending. ---")
            return {"error": "Plan rejected by user."}
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def failure_node(state: ForgeState):
    print("\n🔥 Maximum retries reached. Task failed.")
    return state

planner_agent = PlannerAgent()
coder_agent = CodeGenerationAgent()
tester_agent = TestEngineerAgent()
debugger_agent = DebuggerAgent()

workflow = StateGraph(ForgeState)
workflow.add_node("planner", planner_agent.run)
workflow.add_node("human_review", human_review_node)
workflow.add_node("coder", coder_agent.execute_step)
workflow.add_node("tester", tester_agent.run_tests)
workflow.add_node("debugger", debugger_agent.analyze_error)
workflow.add_node("failure", failure_node)

def review_router(state: ForgeState):
    if state.get("error"):
        return "end"
    else:
        return "coder"

def coder_router(state: ForgeState):
    if state.get("error"):
        return "debugger"
    if state.get("plan") and state.get("current_step", 0) < len(state.get("plan")):
        return "coder"
    else:
        return "tester"

def test_router(state: ForgeState):
    print("---TEST ROUTER---")
    if state.get("error"):
        print(f"---TEST ROUTER: Re-planning due to error: {state.get('error')} ---")
        retries = state.get("retry_count", 0) + 1
        state["retry_count"] = retries

        if retries >= RETRY_LIMIT:
            print("---TEST ROUTER: Maximum retries reached. Routing to failure. ---")
            return "failure"
        else:
            return "replan"
    else:
        print("---TEST ROUTER: Workflow complete. Success! ---")
        return "end"

workflow.set_entry_point("planner")
workflow.add_edge("planner", "human_review")
workflow.add_conditional_edges("human_review", review_router, {"coder": "coder", "end": END})
workflow.add_conditional_edges("coder", coder_router, {"coder": "coder", "tester": "tester", "debugger": "debugger"})
workflow.add_conditional_edges("tester", test_router, {"replan": "planner", "failure": "failure", "end": END})

app = workflow.compile()
print("--- The Forge workflow (with Human-in-the-Loop) is compiled. ---")

async def main():
    parser = argparse.ArgumentParser(description="Run The Forge AI Coder.")
    parser.add_argument("task", type=str, help="The task for the AI to perform.")
    args = parser.parse_args()

    initial_state: ForgeState = {
        "task": args.task,
        "current_step": 0,
        "retry_count": 0
    }

    print(f"\n--- Starting a new run of The Forge (Task: {args.task}) ---")

    config = {"recursion_limit": 50}  # ✅ safely bumped up
    async for event in app.astream(initial_state, config=config):
        for key, value in event.items():
            print(f"--- Event: Node '{key}' ---\n{value}\n")

if __name__ == "__main__":
    asyncio.run(main())
