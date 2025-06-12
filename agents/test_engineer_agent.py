# agents/test_engineer_agent.py

import os
from state import ForgeState
from core.shell_client import ShellClient
from core.venv_resolver import VenvResolver

class TestEngineerAgent:
    def __init__(self):
        self.shell_client = ShellClient()
        self.venv_resolver = VenvResolver()

    async def run_tests(self, state: ForgeState) -> dict:
        print("---TEST ENGINEER: Starting tests...---")

        try:
            task_name = state.get("task", "default_task")
            env_path = self.venv_resolver.get_venv_path(task_name)

            if os.name == 'nt':
                cmd = "set PYTHONPATH=.&& pytest tests"
            else:
                cmd = "PYTHONPATH=. pytest tests"

            env = os.environ.copy()
            env["PYTHONPATH"] = "."

            result = await self.shell_client.run_command(cmd, venv_path=env_path, extra_env=env)

            if "error" in result:
                print("---TEST ENGINEER: ShellClient error detected ---")
                return {"error": result.get("error")}

            if result.get("return_code", 1) == 0:
                print("---TEST ENGINEER: Tests PASSED! ---")
                return {"error": None}
            else:
                print("---TEST ENGINEER: Tests FAILED! ---")
                return {
                    "error": f"pytest failed with the following output:\n\n"
                             f"STDOUT:\n{result.get('stdout')}\n\nSTDERR:\n{result.get('stderr')}"
                }
        except Exception as e:
            return {"error": str(e)}