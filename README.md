# File Integrity Monitor (FIM)

A lightweight, real-time File Integrity Monitoring tool built in Python. It detects unauthorized file changes, deletions, and additions by comparing SHA-256 hashes against a stored baseline — the same core principle used by tools like Tripwire, OSSEC, and Wazuh.

## Why this project

Built as a hands-on way to learn core blue team / SOC concepts: hashing, baselining, continuous monitoring, and alert logging — implemented from scratch in Python using an object-oriented design.

## Features

- SHA-256 hashing of monitored files
- Baseline creation and JSON-based storage
- Detects three types of events:
  - **MODIFIED** — file content changed
  - **DELETED** — file removed
  - **NEW FILE** — file added
- Continuous monitoring loop with configurable interval
- Timestamped alerts logged to `fim_alerts.log`
- Self-exclusion logic (the tool never flags its own log/baseline files)

## Tech Stack

- Python 3
- Standard library only: `hashlib`, `os`, `json`, `time`, `datetime`
- Object-oriented design (`FileIntegrityMonitor` class)

## Installation

```bash
git clone https://github.com/asgerovyunis/file-integrity-monitor.git
cd file-integrity-monitor
```

No external dependencies required — the project only uses Python's standard library.

## Usage

Run the monitor in the folder you want to watch:

```bash
python file_integrity_monitor.py
```

On first run, it creates a `baseline.json` snapshot of the current folder. On every run after that, it compares the live state against the baseline and logs any changes.

Stop monitoring with `Ctrl+C`.

## Output

- **`baseline.json`** — stored hash snapshot of monitored files
- **`fim_alerts.log`** — timestamped log of every detected change

Example log output:
```
[2026-07-09 11:18:56] Baseline created (4 files)
Monitoring started... Press Ctrl+C to stop
[2026-07-09 11:19:21] [DELETED] test.txt
[2026-07-09 11:19:26] [MODIFIED] test4.txt
[2026-07-09 11:19:31] [NEW FILE] test4 (2).txt
```

## How it works

1. **Hashing** — each file's content is hashed with SHA-256, producing a unique fingerprint. Any change to the file content produces a completely different hash.
2. **Baseline** — the initial hash snapshot is stored as the source of truth.
3. **Comparison loop** — on each cycle, the tool rescans the folder, recomputes hashes, and compares them against the baseline to detect modifications, deletions, and new files.
4. **Logging** — every detected event is timestamped and written to both the console and a persistent log file.

## Possible improvements

- Recursive monitoring of subdirectories
- Email/webhook alerting on critical changes
- Configurable file/folder exclusion list via config file
- Multi-threaded monitoring for large directory trees

## License

MIT License — free to use, modify, and share.

## Author

**Yunis Asgarov**
- GitHub: [@asgerovyunis](https://github.com/asgerovyunis)
- LinkedIn: [Yunis Asgarov](https://www.linkedin.com/in/yunisasgarov/)
