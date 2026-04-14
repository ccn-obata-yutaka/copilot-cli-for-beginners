#!/bin/sh
set -eu

INPUT=$(cat)
HOOK_INPUT="$INPUT" python3 - <<'PY'
import json
import os
import pathlib
import re
import subprocess
import sys

raw_input = os.environ.get("HOOK_INPUT", "")
if not raw_input:
    sys.exit(0)

try:
    data = json.loads(raw_input)
except json.JSONDecodeError:
    sys.exit(0)

if not isinstance(data, dict):
    sys.exit(0)
tool_name = data.get("toolName") or data.get("tool_name") or ""
tool_args = data.get("toolArgs") or data.get("tool_input") or {}

if isinstance(tool_args, str):
    try:
        tool_args = json.loads(tool_args)
    except json.JSONDecodeError:
        tool_args = {}

command = tool_args.get("command", "")
if tool_name not in {"bash", "run_in_terminal"}:
    sys.exit(0)

if "git commit" not in command:
    sys.exit(0)

result = subprocess.run(
    ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
    capture_output=True,
    text=True,
    check=True,
)
staged_files = [line.strip() for line in result.stdout.splitlines() if line.strip().endswith(".py")]
pattern = re.compile(r"\.\./|\.\.\\")
suspicious = []

for file_name in staged_files:
    file_path = pathlib.Path(file_name)
    try:
        contents = file_path.read_text(encoding="utf-8")
    except OSError:
        continue
    if pattern.search(contents):
        suspicious.append(file_name)

if suspicious:
    message = "Suspicious path traversal pattern found in: " + ", ".join(suspicious)
    print(json.dumps({
        "permissionDecision": "deny",
        "permissionDecisionReason": message,
    }))
PY
