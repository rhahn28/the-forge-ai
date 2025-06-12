# agents/planner_agent.py
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from state import ForgeState
from core.models import Plan, PlanStep
from core.file_client import FileSystemClient
from typing import List

class PlannerAgent:
    def __init__(self):
        load_dotenv()
        self.pydantic_parser = PydanticOutputParser(pydantic_object=Plan)
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """
You are a hyper-efficient, non-conversational software planning bot. Your sole purpose is to convert user requests into a JSON object that strictly adheres to the provided schema.
DO NOT output any text, introductions, or explanations. You MUST only output the JSON.
The user's request may include feedback from a previous failed attempt. Use this feedback to improve the plan.
You MUST create a 'src/' directory for main code and a 'tests/' directory for test code.
For every script file created, you MUST also create a corresponding test file.
"""),
                ("human", """
User Request: "{task}"
Error Feedback (if any): "{error}"

SCHEMA:
{format_instructions}
"""),
            ]
        )
        self.llm_chain = self.prompt | ChatOpenAI(model="gpt-4o") | self.pydantic_parser

    async def run(self, state: ForgeState) -> dict:
        print("---PLANNER AGENT (Pydantic): Generating a plan...---")
        try:
            plan_obj = await self.llm_chain.ainvoke({
                "task": state['task'],
                "error": state.get("error", "None"),
                "format_instructions": self.pydantic_parser.get_format_instructions(),
            })
            plan_list = [step.model_dump() for step in plan_obj.steps]
            if not plan_list:
                raise ValueError("Planner returned an empty plan.")
            print("---PLANNER AGENT: Plan Generated and Validated.---")
            print(plan_list)
            return {"plan": plan_list, "current_step": 0, "error": None}
        except Exception as e:
            print(f"---PLANNER AGENT: ERROR - {e}---")
            return {"error": f"Planner failed with an unrecoverable error: {e}"}