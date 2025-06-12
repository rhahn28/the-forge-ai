# core/venv_manager.py

import subprocess
import sys
import os
import json
import re
import hashlib
from datetime import datetime, timedelta

class VirtualEnvManager:
    def __init__(self, base_dir="generated_envs", retention_days=30):
        self.base_dir = base_dir
        self.metadata_file = os.path.join(self.base_dir, "venv_metadata.json")
        self.retention_days = retention_days
        os.makedirs(self.base_dir, exist_ok=True)
        self.load_metadata()

    def load_metadata(self):
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, "r") as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}

    def save_metadata(self):
        with open(self.metadata_file, "w") as f:
            json.dump(self.metadata, f, indent=2)

    def create_env(self, env_name_raw):
        env_name = sanitize_task_name(env_name_raw)
        env_path = os.path.join(self.base_dir, env_name)
        if not os.path.exists(env_path):
            print(f"[VENV MANAGER] Creating venv: {env_path}")
            result = subprocess.run(
                [sys.executable, "-m", "venv", env_path],
                capture_output=True, text=True
            )
            print(f"[VENV MANAGER] venv stdout: {result.stdout}")
            print(f"[VENV MANAGER] venv stderr: {result.stderr}")
            result.check_returncode()  # <-- crash immediately if subprocess fails
            print(f"✅ Created virtual environment at: {env_path}")

            self.metadata[env_name] = {
                "path": env_path,
                "created": datetime.utcnow().isoformat(),
                "libraries": [],
                "task_raw_name": env_name_raw
            }
            self.save_metadata()
        else:
            print(f"✅ Virtual environment already exists: {env_path}")
        return env_path

    def install_package(self, env_path, package_name, env_name_raw):
        env_name = sanitize_task_name(env_name_raw)
        pip_path = os.path.join(env_path, "bin", "pip") if os.name != "nt" else os.path.join(env_path, "Scripts", "pip.exe")
        
        print(f"[VENV MANAGER] Installing package '{package_name}' into venv: {env_path}")

        result = subprocess.run(
            [pip_path, "install", package_name],
            capture_output=True, text=True
        )
        print(f"[VENV MANAGER] pip stdout: {result.stdout}")
        print(f"[VENV MANAGER] pip stderr: {result.stderr}")
        result.check_returncode()

        if env_name in self.metadata:
            if package_name not in self.metadata[env_name]["libraries"]:
                self.metadata[env_name]["libraries"].append(package_name)
                self.save_metadata()

    def get_env_path(self, env_name_raw):
        env_name = sanitize_task_name(env_name_raw)
        return os.path.join(self.base_dir, env_name)

    def get_env_metadata(self, env_name_raw):
        env_name = sanitize_task_name(env_name_raw)
        return self.metadata.get(env_name, {})

    def delete_env(self, env_name_raw):
        env_name = sanitize_task_name(env_name_raw)
        env_path = self.get_env_path(env_name)
        if os.path.exists(env_path):
            subprocess.run(["rm", "-rf", env_path])
            print(f"✅ Deleted virtual environment: {env_path}")
        if env_name in self.metadata:
            del self.metadata[env_name]
            self.save_metadata()

    def clean_all_envs(self):
        for env_name in list(self.metadata.keys()):
            self.delete_env(env_name)

    def garbage_collect_old_envs(self):
        print("Running garbage collection on virtual environments...")
        cutoff = datetime.utcnow() - timedelta(days=self.retention_days)
        for env_name, meta in list(self.metadata.items()):
            created_date = datetime.fromisoformat(meta['created'])
            if created_date < cutoff:
                print(f"Deleting old environment: {env_name}")
                self.delete_env(env_name)


# ✅ Safe task name sanitizer
def sanitize_task_name(task_name, max_length=64):
    safe = re.sub(r'[^a-zA-Z0-9]+', '_', task_name)
    if len(safe) > max_length:
        hash_suffix = hashlib.sha1(task_name.encode()).hexdigest()[:8]
        safe = safe[:max_length] + "_" + hash_suffix
    return safe
