# agents/test_engineer_agent.py
from state import ForgeState
from core.shell_client import ShellClient

class TestEngineerAgent:
    """
    This agent runs tests and provides specific, machine-readable feedback.
    """
    def __init__(self):
        self.shell_client = ShellClient()

    async def run_tests(self, state: ForgeState) -> dict:
        print("---TEST ENGINEER: Starting tests...---")
        try:
            result = await self.shell_client.run_command("pytest")
            stdout = result.get("stdout", "")
            
            if result.get("return_code") == 0:
                print("---TEST ENGINEER: All tests passed! ---")
                print(stdout)
                return {"result": "All tests passed."}
            else:
                print("---TEST ENGINEER: Tests FAILED! ---")
                # --- CORRECTED ERROR CHECKING ---
                # We now look for the "collected 0 items" string from pytest's output.
                if "collected 0 items" in stdout:
                    error_message = "pytest: No tests were found."
                else:
                    stderr = result.get("stderr", "")
                    error_message = f"pytest failed with the following output:\n\nSTDOUT:\n{stdout}\n\nSTDERR:\n{stderr}"
                
                print(error_message)
                return {"error": error_message}
        except Exception as e:
            error_message = f"An error occurred running tests: {e}"
            print(f"---TEST ENGINEER: ERROR - {error_message}---")
            return {"error": error_message}