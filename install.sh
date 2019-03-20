#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

echo "export HISTIGNORE=\"history -a; eval*\":\$HISTIGNORE" >> ~/.bashrc
echo "bind '\"\C-e\"':\"\\\"history -a; eval \\$\(${DIR}/search_history.py\) \C-m\\\"\"" >> ~/.bashrc

echo ~/.bashrc updated. CTRL+E shortcut will be available in new 
echo terminals. 

