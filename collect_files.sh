#!/bin/bash

if [ "$#" -lt 2 ]; then
    echo "ERROR. Правильное использование: ./collect_files.sh input_dir_path output_dir_path [--max_depth n]"
    exit 1
fi

input_dir="$1"
output_dir="$2"
max_depth=999

if [ "$#" -eq 4 ] && [ "$3" == "--max_depth" ]; then
    max_depth="$4"
fi

mkdir -p "$output_dir"

python3 collect_files.py "$input_dir" "$output_dir" "$max_depth"
