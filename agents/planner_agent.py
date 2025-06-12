# agents/planner_agent.py
import httpx
import json
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from state import ForgeState
from core.file_client import FileSystemClient


class PlannerAgent:
    """
    This agent uses an LLM to generate a detailed, structured JSON plan.
    """
    def __init__(self):
        load_dotenv()
        self.fs_client = FileSystemClient()
        
        prompt_template = """
You are a code generation bot. Your sole purpose is to convert a user's request into a series of commands in a JSON format.
You MUST ONLY output a valid JSON list of objects, even if the plan only contains one step.

The user's request is: "{task}"
The current files in the directory are: "{files}"

Each object in the JSON list MUST have a "command" key and a "path" key.
If the command is "WRITE_TO_FILE", it MUST also include a "content" key.
The only valid commands are "CREATE_FILE" and "WRITE_TO_FILE".

This is an example of a valid response for a multi-step plan:
```json
[
    {{
        "command": "CREATE_FILE",
        "path": "example.py"
    }},
    {{
        "command": "WRITE_TO_FILE",
        "path": "example.py",
        "content": "print('This is an example')"
    }}
]

This is an example of a valid response for a single-step plan:

[
    {{
        "command": "CREATE_FILE",
        "path": "single_file.py"
    }}
]




NOW, GENERATE THE PLAN FOR THE USER'S REQUEST. Output ONLY the JSON list, inside a ```json code block.
"""

        # --- Instruction 4 in the recipe ---
        # Because this line has the same indentation, it is the very next step
        # in the same recipe. Python now creates an attribute on our object
        # called 'self.llm_chain'. To do this, it USES the 'prompt_template'
        # variable it created in the step right above.
        self.llm_chain = (
            ChatPromptTemplate.from_template(prompt_template)
            | ChatOpenAI(model="gpt-4o", response_format={"type": "json_object"})
            | StrOutputParser()
        )
    
    # Now the recipe for __init__ is finished.
    # This 'run' method is also part of the PlannerAgent class, but it's a different recipe.




    async def run(self, state: ForgeState) -> dict:
        """
        This is the main entry point for the agent's logic.
        """
        print("---PLANNER AGENT (JSON): Generating a plan...---")
        plan_str = ""
        try:
            current_files = await self.fs_client.list_files()
            plan_str = await self.llm_chain.ainvoke({
                "task": state['task'],
                "files": ", ".join(current_files) if current_files else "No files yet."
            })
            
            parsed_json = json.loads(plan_str)
            
            # --- NEW ROBUST LOGIC ---
            # If the AI returns a single dictionary instead of a list of dictionaries,
            # we will automatically wrap it in a list to handle the case.
            if isinstance(parsed_json, dict):
                # Check if it's a plan list nested under a key
                if len(parsed_json) == 1 and isinstance(next(iter(parsed_json.values())), list):
                    plan_list = next(iter(parsed_json.values()))
                else: # It's a single command object
                    print("---INFO: AI returned a single command object. Wrapping it in a list.---")
                    plan_list = [parsed_json]
            elif isinstance(parsed_json, list):
                plan_list = parsed_json
            else:
                raise ValueError("Parsed JSON is not a recognized format (list or dict).")
            # --- END OF NEW LOGIC ---

            print("---PLANNER AGENT: Plan Generated.---")
            print(plan_list)
            
            return {"plan": plan_list, "current_step": 0}
        except Exception as e:
            print(f"---PLANNER AGENT: ERROR - {e}---")
            print("---RAW LLM OUTPUT THAT CAUSED ERROR:---")
            print(plan_str)
            print("---------------------------------------")
            return {"error": str(e)}