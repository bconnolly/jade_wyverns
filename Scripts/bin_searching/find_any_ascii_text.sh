#!/bin/bash
# Usage: ./extract_strings.sh <folder>

if [ -z "$1" ]; then
	  echo "Usage: $0 <folder>"
	    exit 1
fi

search_dir="$1"

if [ ! -d "$search_dir" ]; then
	  echo "Error: '$search_dir' is not a directory"
	    exit 1
fi

# Prepare output directory and unique timestamped filename
script_dir="$(dirname "$0")"
output_dir="$script_dir/results"
mkdir -p "$output_dir"

timestamp=$(date +"%Y-%m-%d_%H-%M-%S")
output_file="$output_dir/strings_$timestamp.csv"

# Write CSV header (overwrite just in case, file is new anyway)
echo '"file","string"' > "$output_file"

# Extract ASCII strings from every file and append to CSV
find "$search_dir" -type f | xargs -P "$(nproc)" -I {} bash -c '
  file="{}"
    while IFS= read -r line; do
	        safe_line="${line//\"/\"\"}"   # escape double quotes
		    safe_file="${file//\"/\"\"}"
		        echo "\"$safe_file\",\"$safe_line\""
			  done < <(strings "$file")
			  ' >> "$output_file"

			  echo "Done! Results saved to: $output_file"

