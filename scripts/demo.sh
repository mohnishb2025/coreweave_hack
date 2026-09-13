#!/usr/bin/env bash
set -euo pipefail

case_id="${1:-}"
model_id="${2:-}"
if [[ -z "$case_id" || -z "$model_id" ]]; then
  echo "Usage: $0 CASE_ID MODEL_ID" >&2
  exit 2
fi

repair-loop models
repair-loop cases
REPAIR_LOOP_REMOTE_EXECUTION=1 repair-loop repair \
  "$case_id" --model "$model_id" --variant full_team --max-attempts 3

echo "Open the Codespaces lab with:"
echo "marimo run --host 0.0.0.0 --port 2718 notebooks/repair_lab.py"
