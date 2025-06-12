# agents/debugger_agent.py
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from state import ForgeState

class DebuggerAgent:
    def __init__(self):
        load_dotenv()
        prompt_template = """
You are an expert software debugger. A test run has failed. Analyze the original task and the pytest error to provide a concise, one-sentence recommendation for the Planner on how to fix the code.

Original Task: "{task}"
Pytest Error Log:

{error}

YBased on the error, your recommendation for the planner is:
"""
        self.llm_chain = (
            ChatPromptTemplate.from_template(prompt_template)
            | ChatOpenAI(model="gpt-4o")
            | StrOutputParser()
        )
    
    async def analyze_error(self, state: ForgeState) -> dict:
        print("---DEBUGGER AGENT: Analyzing test failure...---")

        prompt_template = """
        You are an expert software debugger. A step in the plan has failed. Analyze the original task, the failed step, and the resulting error to provide a concise, one-sentence recommendation for the Planner on how to fix the plan.

        Original Task: "{task}"
        Failed Step: "{failed_step}"
        Error Log: "{error}"

        Your recommendation for the planner is:
        """


        try:
            recommendation = await self.llm_chain.ainvoke({
                "task": state['task'],
                "error": state['error'],
            })
            print(f"---DEBUGGER AGENT: Recommendation: {recommendation}---")
            # We overwrite the old error with this new, specific feedback for the planner
            return {"error": recommendation}
        except Exception as e:
            print(f"---DEBUGGER AGENT: ERROR - {e}---")
            return {"error": f"Failed to analyze error: {e}"}

