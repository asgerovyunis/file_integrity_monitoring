import os
import hashlib
import json
import time
from datetime import datetime


class FileIntegrityMonitor:
    def __init__(self, folder=".", baseline_file="baseline.json", log_file="fim_alerts.log"):
        self.folder = folder
        self.baseline_file = baseline_file
        self.log_file = log_file
        self.excluded = {self.baseline_file, self.log_file}
        self.baseline = {}

    def _get_file_hash(self, filepath):
        with open(filepath, "rb") as f:
            content = f.read()
        return hashlib.sha256(content).hexdigest()

    def _timestamp(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _log(self, message):
        print(message)
        with open(self.log_file, "a") as f:
            f.write(message + "\n")

    def scan(self):
        current = {}
        for filename in os.listdir(self.folder):
            if filename.endswith(".py") or filename in self.excluded:
                continue
            filepath = os.path.join(self.folder, filename)
            if os.path.isfile(filepath):
                current[filename] = self._get_file_hash(filepath)
        return current

    def create_baseline(self):
        self.baseline = self.scan()
        with open(self.baseline_file, "w") as f:
            json.dump(self.baseline, f, indent=4)
        self._log(f"[{self._timestamp()}] Baseline created ({len(self.baseline)} files)")

    def load_baseline(self):
        with open(self.baseline_file, "r") as f:
            self.baseline = json.load(f)

    def check_once(self):
        current = self.scan()
        changes_found = False

        for filename in self.baseline:
            if filename not in current:
                self._log(f"[{self._timestamp()}] [DELETED] {filename}")
                changes_found = True
            elif self.baseline[filename] != current[filename]:
                self._log(f"[{self._timestamp()}] [MODIFIED] {filename}")
                changes_found = True

        for filename in current:
            if filename not in self.baseline:
                self._log(f"[{self._timestamp()}] [NEW FILE] {filename}")
                changes_found = True

        if not changes_found:
            self._log(f"[{self._timestamp()}] No changes detected, all files OK")

        self.baseline = current

    def run(self, interval=5):
        print("Monitoring started... Press Ctrl+C to stop")
        while True:
            self.check_once()
            time.sleep(interval)


if __name__ == "__main__":
    monitor = FileIntegrityMonitor(folder=".")

    # Create a baseline if one doesn't exist yet
    if not os.path.exists(monitor.baseline_file):
        monitor.create_baseline()
    else:
        monitor.load_baseline()

    monitor.run(interval=5)
