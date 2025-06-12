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
    "PYTHONPATH=.",
    "PYTHONPATH=.;src",      # ← Add this for Windows
    "PYTHONPATH=.:src",      # ← Add this for Linux/Mac
    "set PYTHONPATH=src&&",
    "set PYTHONPATH=.&&",
    "set PYTHONPATH=.;src&&", # ← Add this for Windows
    "set PYTHONPATH=.:src&&", # ← Add this for Linux/Mac
    "set PYTHONPATH=src &&",
    "set PYTHONPATH=. &&",
    "set PYTHONPATH=.;src &&", # ← Add this for Windows
    "set PYTHONPATH=.:src &&"  # ← Add this for Linux/Mac
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

    # Replace this entire section:
    allow = any(command_to_run.startswith(prefix) for prefix in SAFE_PREFIXES)

    # With this more flexible check:
    def is_safe_command(cmd):
        # Allow pytest commands
        if "pytest" in cmd:
            return True
        # Allow PYTHONPATH setting
        if "PYTHONPATH=" in cmd:
            return True
        # Allow pip commands  
        if cmd.startswith("pip"):
            return True
        # Allow python commands
        if cmd.startswith("python"):
            return True
        return False

    allow = is_safe_command(command_to_run)

    env = os.environ.copy()
    env.update(extra_env)

    # tools/mcp_server_shell.py  (partial inside run_shell_command)

    try:
        env = os.environ.copy()
        env.update(extra_env)
        
        # 🔧 FIX: Better working directory detection
        working_dir = os.getcwd()  # Use current working directory instead of relative path
        print(f"---SHELL SERVER: Working directory: {working_dir}---")
        
    # In the run_shell_command function, replace the venv activation section with:

        if venv_path:
            if os.name == "nt":
                python_exe = os.path.join(venv_path, "Scripts", "python.exe")
                # Replace the command to use venv python directly
                if command_to_run.startswith("set PYTHONPATH="):
                    # Extract the actual command after &&
                    parts = command_to_run.split("&&", 1)
                    if len(parts) == 2:
                        pythonpath_part = parts[0].strip()
                        actual_command = parts[1].strip()
                        # Set PYTHONPATH in env and use venv python
                        if "PYTHONPATH=" in pythonpath_part:
                            path_value = pythonpath_part.split("=", 1)[1]
                            env["PYTHONPATH"] = path_value
                        
                        # Use venv python with -m pytest
                        if actual_command.startswith("pytest"):
                            new_command = f'"{python_exe}" -m {actual_command}'
                        else:
                            new_command = f'"{python_exe}" -c "import os; os.system({repr(actual_command)})"'
                        
                        print(f"---SHELL SERVER: Using venv python: {new_command}---")
                        result = subprocess.run(new_command, capture_output=True, text=True, shell=True, env=env, cwd=working_dir)
                else:
                    result = subprocess.run(command_to_run, capture_output=True, text=True, shell=True, env=env, cwd=working_dir)
            else:
                # Similar logic for Linux/Mac
                python_exe = os.path.join(venv_path, "bin", "python")
                # Add Linux/Mac handling here
                result = subprocess.run(command_to_run, capture_output=True, text=True, shell=True, env=env, cwd=working_dir)
        else:
            result = subprocess.run(command_to_run, capture_output=True, text=True, shell=shell, env=env, cwd=working_dir)


    except Exception as e:
        print(f"ERROR: Failed to execute command '{command_to_run}': {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    print("Starting Shell MCP Server on http://127.0.0.1:8001")
    uvicorn.run(app, host="127.0.0.1", port=8001)
