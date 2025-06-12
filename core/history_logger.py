# core/history_logger.py

import json
import os
from datetime import datetime

class HistoryLogger:
    def __init__(self, logfile="forge_history.jsonl"):
        self.logfile = logfile

    def append_entry(self, entry):
        entry["timestamp"] = datetime.utcnow().isoformat()
        with open(self.logfile, "a") as f:
            f.write(json.dumps(entry) + "\n")
        print(f"✅ History entry logged.")

    def read_all(self):
        with open(self.logfile, "r") as f:
            return [json.loads(line) for line in f]
