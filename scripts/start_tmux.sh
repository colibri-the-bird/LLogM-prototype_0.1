#!/usr/bin/env bash
set -euo pipefail

SESSION=llogm
if ! tmux has-session -t $SESSION 2>/dev/null; then
  tmux new-session -d -s $SESSION -n dev
  tmux send-keys -t $SESSION 'cd /workspace/llogm && source .venv/bin/activate' C-m
fi

echo "Attach with: tmux attach -t $SESSION"
