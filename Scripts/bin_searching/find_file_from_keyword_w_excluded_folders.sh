#!/bin/bash


search_dir="vanilla_out"
phrase="$1"

if [ ! -d "$search_dir" ]; then
	  echo "Error: '$search_dir' is not a directory"
	    exit 1
fi

# List of folder names to skip (just names, not full paths)
EXCLUDE=("narration_script" "narration_script_text_eng_u" "narration_script_text_non_u_english" "opening_credits")

# Build the find command with pruning
find_cmd=(find "$search_dir")

# Add prune rules
for excl in "${EXCLUDE[@]}"; do
	  find_cmd+=(-type d -name "$excl" -prune -o)
  done

  # Finish with: type f -print
  find_cmd+=(-type f -print)

  # Clean phrase
  clean_phrase=$(echo -n "$phrase" | tr -d '\0\n')

  # Run search in parallel
  "${find_cmd[@]}" | xargs -P "$(nproc)" -I {} bash -c '
    file="{}"
      if tr -d "\0\n" < "$file" 2>/dev/null | grep -qF "$0"; then
	          echo "Found in: $file"
		    fi
		    ' "$clean_phrase"

