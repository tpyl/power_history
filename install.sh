#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "export HISTIGNORE=\"history -a; CMD*\":\$HISTIGNORE" >> ~/.bashrc
echo "bind '\"\C-e\"':\"'history -a; CMD=\\$\(${DIR}/search_history.py \\\$COLUMNS\); history -s \\\"\\\$CMD\\\"; \C-m\e[A'\"" >> ~/.bashrc

echo ~/.bashrc updated. CTRL+E shortcut will be available in new 
echo terminals. 

