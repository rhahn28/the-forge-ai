# agents/planner_agent.py
import httpx # The library for making network requests to our tool server.
from state import ForgeState # We import our central state definition.

class FileSystemClient:
    """
    This is the agent's 'remote control' for the FileSystemMCPServer.
    It's a dedicated client that knows how to format requests and talk to our tool.
    This keeps networking logic separate from the agent's core 'thinking' logic.
    """
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    async def read_file(self, path: str):
        # Use httpx to create an asynchronous client session.
        async with httpx.AsyncClient() as client:
            print(f"CLIENT: Sending READ request for '{path}' to {self.base_url}")
            # Send a POST request to the server's /read_file endpoint.
            response = await client.post(f"{self.base_url}/read_file", json={"path": path})
            # This will automatically raise an error if the server returns a bad status (like 404 or 500).
            response.raise_for_status()
            # Return the 'content' part of the JSON response from the server.
            return response.json()['content']

    async def write_file(self, path: str, content: str):
        async with httpx.AsyncClient() as client:
            print(f"CLIENT: Sending WRITE request for '{path}' to {self.base_url}")
            response = await client.post(f"{self.base_url}/write_file", json={"path": path, "content": content})
            response.raise_for_status()
            return response.json()

class PlannerAgent:
    """
    This class contains the agent's core logic.
    For Phase 1, its job is simple: read a file and write a file.
    """
    def __init__(self):
        # The agent creates an instance of its tool client. It now "has a" remote control.
        self.fs_client = FileSystemClient()

    async def run(self, state: ForgeState) -> dict:
        """
        This is the main entry point for the agent's logic.
        LangGraph will call this function and pass it the current state.
        """
        # This is our new debugging line to see if the agent's code is even being called.
        print("DEBUG: PlannerAgent.run() method has been called.")
        print("---PLANNER AGENT: Starting operation.---")
        
        # 1. Read the initial task from the state dictionary.
        input_file = state['task']
        output_file = "plan.txt" # We'll hardcode the output file for now.
        
        try:
            # 2. Use the tool client to perform the first action.
            content = await self.fs_client.read_file(input_file)
            
            # 3. Use the tool client to perform the second action.
            await self.fs_client.write_file(output_file, f"PLAN FROM FILE:\n{content}")
            
            result_message = f"Successfully processed '{input_file}' to '{output_file}'."
            print("---PLANNER AGENT: Finished successfully.---")

            # 4. Return a dictionary to update the central state.
            return {"result": result_message}
            
        except Exception as e:
            error_message = f"An error occurred: {e}"
            print(f"---PLANNER AGENT: {error_message}---")
            # If something goes wrong, update the 'error' field in the state.
            return {"error": error_message}