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

python3 <<EOF
import os
import shutil
import sys

input_dir = "$input_dir"
output_dir = "$output_dir"
max_depth = int($max_depth)


def copy_files(src, dest, max_depth, depth=0):

	if depth > max_depth:
		return
	if not os.path.exists(src):
		return
	if os.path.isfile(src):
		filename = os.path.basename(src)
		dest_path = os.path.join(dest, filename)
		duplicates = 1

		while os.path.exists(dest_path):
			name, ext = os.path.splitext(filename)
			dest_path = os.path.join(dest, f"{name}{duplicates}{ext}")
			duplicates += 1

		shutil.copy2(src, dest_path)
	elif os.path.isdir(src):
		if depth < max_depth:
			for item in os.listdir(src):
				item_path = os.path.join(src, item)
				copy_files(item_path, dest, max_depth, depth + 1)

copy_files(input_dir, output_dir, max_depth)

EOF
