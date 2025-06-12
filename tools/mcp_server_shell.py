# tools/mcp_server_shell.py

import subprocess
import shlex
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

SAFE_PREFIXES = [
    "pytest",
    "PYTHONPATH=src",
    "set PYTHONPATH=src&&"
]

class ShellPayload(BaseModel):
    command: str
    venv_path: str = None
    extra_env: dict = None

@app.post("/run_shell")
async def run_shell_command(payload: ShellPayload):
    command_to_run = payload.command
    venv_path = payload.venv_path
    extra_env = payload.extra_env or {}

    print(f"---SHELL SERVER: Received command: '{command_to_run}'---")
    print(f"---SHELL SERVER: Extra env: {extra_env}---")

    allow = any(command_to_run.startswith(prefix) for prefix in SAFE_PREFIXES)
    if not allow:
        print(f"---SHELL SERVER: REJECTED forbidden command '{command_to_run}'---")
        raise HTTPException(status_code=403, detail=f"Command '{command_to_run}' is not allowed.")

    env = os.environ.copy()
    env.update(extra_env)

    # tools/mcp_server_shell.py  (partial inside run_shell_command)

    try:
        env = os.environ.copy()
        env.update(extra_env)

        # Detect correct working directory (adjust this as needed)
        working_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        if venv_path:
            if os.name == "nt":
                activate_path = os.path.join(venv_path, "Scripts", "activate.bat")
                full_command = f'cmd /c "{activate_path} && {command_to_run}"'
            else:
                activate_path = os.path.join(venv_path, "bin", "activate")
                full_command = f'bash -c "source \'{activate_path}\' && {command_to_run}"'

            print(f"---SHELL SERVER: Full venv command: {full_command}---")
            result = subprocess.run(full_command, capture_output=True, text=True, shell=True, env=env, cwd=working_dir)
        else:
            result = subprocess.run(command_to_run, capture_output=True, text=True, shell=True, env=env, cwd=working_dir)

        return {
            "status": "success",
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }


    except Exception as e:
        print(f"ERROR: Failed to execute command '{command_to_run}': {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting Shell MCP Server on http://127.0.0.1:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001)
