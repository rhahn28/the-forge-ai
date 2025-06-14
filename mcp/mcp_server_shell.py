# mcp/mcp_server_shell.py
import subprocess
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class ShellPayload(BaseModel):
    command: str
    # The 'venv' key now expects the *name* of the conda env, e.g., "forgeenv"
    venv: str 

@app.post("/run_in_venv")
async def run_shell_in_venv(payload: ShellPayload):
    command_to_run = payload.command
    venv_name = payload.venv
    print(f"---SHELL SERVER: Rcvd request to run '{command_to_run}' in venv '{venv_name}'---")
    try:
        # 'conda run' is the most reliable way to execute a command in a specific env
        full_command = f'conda run -n "{venv_name}" {command_to_run}'
        print(f"---SHELL SERVER: Executing full command: {full_command}---")
        result = subprocess.run(
            full_command, capture_output=True, text=True, shell=True, check=False
        )
        print(f"---SHELL SERVER: Command finished with code {result.returncode}---")
        return {
            "status": "success", "return_code": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)