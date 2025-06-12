# core/task_metadata.py

import json
import os
from datetime import datetime

class TaskMetadataLogger:
    def __init__(self, base_dir="task_logs"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def log_task(self, task_id, metadata):
        filename = os.path.join(self.base_dir, f"{task_id}.json")
        metadata["timestamp"] = datetime.utcnow().isoformat()
        with open(filename, "w") as f:
            json.dump(metadata, f, indent=2)
        print(f"✅ Logged task metadata: {filename}")

    def list_tasks(self):
        return [f for f in os.listdir(self.base_dir) if f.endswith(".json")]

    def load_task(self, task_id):
        filename = os.path.join(self.base_dir, f"{task_id}.json")
        if os.path.exists(filename):
            with open(filename, "r") as f:
                return json.load(f)
        return None
