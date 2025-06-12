import asyncio
import os
import argparse
from langgraph.graph import StateGraph, END
from state import ForgeState
from agents.planner_agent import PlannerAgent
from agents.code_generator_agent import CodeGenerationAgent
from agents.test_engineer_agent import TestEngineerAgent
from agents.debugger_agent import DebuggerAgent

def human_review_node(state: ForgeState):
    print("=== HUMAN REVIEW ===")
    plan = state.get("plan")
    if not plan:
        return {"error": "No plan generated."}
   
    print(f"Plan has {len(plan)} steps")
    for i, step in enumerate(plan):
        print(f"  Step {i+1}: {step}")
    user_input = input("Approve? (y/n): ").lower().strip()
    if user_input == 'y':
        return {"error": None}
    else:
        return {"error": "Plan rejected."}

def success_node(state: ForgeState):
    print("✅ TASK COMPLETED SUCCESSFULLY!")
    return {"status": "SUCCESS"}

# Initialize agents
planner_agent = PlannerAgent()
coder_agent = CodeGenerationAgent()
tester_agent = TestEngineerAgent()

# Create workflow
workflow = StateGraph(ForgeState)
workflow.add_node("planner", planner_agent.run)
workflow.add_node("human_review", human_review_node)
workflow.add_node("coder", coder_agent.execute_step)
workflow.add_node("success", success_node)

# Simple routing - FIXED
def coder_router(state: ForgeState):
    plan = state.get("plan", [])
    current_step = state.get("current_step", 0)
   
    if current_step < len(plan):
        return "coder"
    else:
        return "success"  # Changed to success

workflow.set_entry_point("planner")
workflow.add_edge("planner", "human_review")
workflow.add_edge("human_review", "coder")
workflow.add_conditional_edges("coder", coder_router, {"coder": "coder", "success": "success"})
workflow.add_edge("success", END)

app = workflow.compile()

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task", type=str)
    args = parser.parse_args()
    initial_state = {"task": args.task, "current_step": 0}
   
    async for event in app.astream(initial_state, config={"recursion_limit": 50}):
        for key, value in event.items():
            print(f"=== {key} ===")
            print(value)

if __name__ == "__main__":
    asyncio.run(main())