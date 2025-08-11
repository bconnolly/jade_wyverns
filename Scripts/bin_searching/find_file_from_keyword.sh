#!/bin/bash

# Find file from keyword
# By: Lilypad

# This script takes a phrase and searches the vanilla_out folder for the text
# It is recommended you use WSL1 or WSL2 for this, as the script is fairly resource intenstive. 
# Use WSL1 if you are a VirtualBox user, as WSL2 requires HyperV to be enabled. VirtualBox requires HyperV to be disabled.

# args - phrase to search
# output- echos the matches

phrase=$1

search_dir="./vanilla_out"
clean_phrase=$(echo -n "$phrase" | tr -d '\0\n')

find "$search_dir" -type f | xargs -P "$(nproc)" -I {} bash -c '
  file="{}"
  if tr -d "\0\n" < "$file" | grep -oF "$0"; then
    echo "Found in: $file"
  fi
' "$clean_phrase"
