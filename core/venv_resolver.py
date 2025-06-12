# core/venv_resolver.py

import os
from core.venv_manager import sanitize_task_name

class VenvResolver:
    def __init__(self, base_dir="generated_envs"):
        self.base_dir = base_dir

    def get_venv_path(self, task_name: str):
        safe_task_name = sanitize_task_name(task_name)
        env_path = os.path.join(self.base_dir, safe_task_name)
        return env_path

