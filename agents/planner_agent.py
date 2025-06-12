# agents/planner_agent.py
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from state import ForgeState
from core.models import Plan, PlanStep # We now use both
from typing import List

class PlannerAgent:
    def __init__(self):
        load_dotenv()
        # The parser now uses the Plan model, which contains the smart validators
        self.pydantic_parser = PydanticOutputParser(pydantic_object=Plan)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a hyper-efficient software planning bot. Your sole purpose is to convert user requests into a JSON object that strictly adheres to the provided schema. DO NOT output any text, introductions, or explanations. You MUST only output the JSON. Use the feedback from previous errors to improve the plan."""),
            ("human", "User Request: \"{task}\"\nError Feedback (if any): \"{error}\"\n\nSCHEMA:\n{format_instructions}"),
        ])
        self.llm_chain = self.prompt | ChatOpenAI(model="gpt-4o") | self.pydantic_parser

    async def run(self, state: ForgeState) -> dict:
        print("---PLANNER AGENT (Pydantic Validator): Generating a plan...---")
        try:
            plan_obj = await self.llm_chain.ainvoke({
                "task": state['task'], "error": state.get("error", "None"),
                "format_instructions": self.pydantic_parser.get_format_instructions(),
            })
            plan_list = [step.model_dump() for step in plan_obj.steps]
            print("---PLANNER AGENT: Plan Generated and Validated by Pydantic.---")
            print(plan_list)
            return {"plan": plan_list, "current_step": 0, "error": None}
        except Exception as e:
            print(f"---PLANNER AGENT: ERROR - {e}---")
            # If Pydantic fails validation, the error is caught here and sent back for a re-plan.
            return {"error": f"Planner failed to generate a valid plan: {e}"}