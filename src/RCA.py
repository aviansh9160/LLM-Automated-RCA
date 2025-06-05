import os
from pathlib import Path
from datetime import datetime
from RCAEngine import call_gemini_for_rca

# Constants
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / "logs"
FILTERED_DIR = BASE_DIR / "outputs" / "filtered"
FILTERED_DIR.mkdir(parents=True, exist_ok=True)


# Filter keywords for RCA
FILTER_KEYWORDS = [
    "error", "fail", "failed", "fatal", "exception", "critical",
    "unauthorized", "denied", "refused", "unavailable", "timeout"
]

def read_log_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.readlines()
    except Exception as e:
        print(f"[!] Failed to read {file_path.name}: {e}")
        return []

def filter_log_lines(log_lines):
    return [
        line.strip() for line in log_lines
        if any(keyword in line.lower() for keyword in FILTER_KEYWORDS)
    ]

def save_filtered_output(file_name, filtered_lines):
    output_file = FILTERED_DIR / f"{file_name}_filtered.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(filtered_lines))
    print(f"[+] Saved filtered logs to: {output_file.name}")


def process_all_logs():
    log_files = list(LOG_DIR.glob("*.log")) + list(LOG_DIR.glob("*.txt"))
    if not log_files:
        print("[!] No log files found.")
        return

    for log_file in log_files:
        print(f"\n[+] Processing: {log_file.name}")
        lines = read_log_file(log_file)
        filtered = filter_log_lines(lines)
        print(f"  - Total lines: {len(lines)}, Filtered: {len(filtered)}")
        save_filtered_output(log_file.stem, filtered)


def process_filtered_logs():
    for filtered_file in FILTERED_DIR.glob("*_filtered.txt"):
        with open(filtered_file, "r") as f:
            log_lines = f.readlines()

        if log_lines:
            print(f"[+] Sending {filtered_file.name} to Gemini RCA...")
            call_gemini_for_rca(log_lines, filtered_file.stem.replace("_filtered", ""))

if __name__ == "__main__":
    process_all_logs()
    process_filtered_logs()
