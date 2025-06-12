# tools/mcp_server_shell.py
import subprocess
import shlex
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# --- THE FIX IS HERE ---
# This list explicitly allows both 'pytest' and 'pip' as valid commands.
COMMAND_ALLOW_LIST = ["pytest", "pip"]

class ShellPayload(BaseModel):
    command: str

@app.post("/run_shell")
async def run_shell_command(payload: ShellPayload):
    command_to_run = payload.command
    print(f"---SHELL SERVER: Received command: '{command_to_run}'---")

    # This robust parsing correctly identifies the main command (e.g., 'pip').
    try:
        command_parts = shlex.split(command_to_run)
        if not command_parts or command_parts[0] not in COMMAND_ALLOW_LIST:
            # If the command is not allowed, raise a 403 Forbidden error.
            print(f"---SHELL SERVER: REJECTED forbidden command '{command_parts[0]}'---")
            raise HTTPException(
                status_code=403,
                detail=f"Command '{command_parts[0]}' is not in the allow list."
            )
    except Exception as e:
         raise HTTPException(status_code=400, detail=f"Failed to parse command: {e}")

    print(f"---SHELL SERVER: EXECUTING allowed command: {command_to_run}---")
    try:
        result = subprocess.run(
            command_parts, capture_output=True, text=True, check=False
        )
        return {
            "status": "success", "return_code": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr,
        }
    except Exception as e:
        print(f"ERROR: Failed to execute command '{command_to_run}': {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting Shell MCP Server on http://127.0.0.1:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001)