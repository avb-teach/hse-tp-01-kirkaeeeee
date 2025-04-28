import os
import shutil
import sys
from pathlib import Path


def unique_filename(path):
    base, ext = os.path.splitext(path)
    duplicates = 1
    new_path = path
    while os.path.exists(new_path):
        new_path = f"{base}{duplicates}{ext}"
        duplicates += 1
    return new_path


def collect_files_with_depth(src_dir: str, dst_dir: str, max_depth: int) -> None:
    src_dir = Path(src_dir).resolve()
    dst_dir = Path(dst_dir).resolve()

    if not src_dir.is_dir():
        raise ValueError(f"{src_dir}: dir does not exist")

    dst_dir.mkdir(parents=True, exist_ok=True)

    created_dirs = set()

    for root, _, files in os.walk(src_dir):
        current_path = Path(root)

        for file in files:
            src_file = current_path / file
            file_relative_path = src_file.relative_to(src_dir)
            depth = len(file_relative_path.parts)

            if depth <= max_depth:
                target_file_path = dst_dir.joinpath(*file_relative_path.parts)
            else:
                trimmed_parts = file_relative_path.parts[depth - max_depth:-1]
                target_file_path = dst_dir.joinpath(*trimmed_parts, file)

            parent_dir = target_file_path.parent

            if parent_dir not in created_dirs:
                parent_dir.mkdir(parents=True, exist_ok=True)
                created_dirs.add(parent_dir)

            shutil.copy2(src_file, target_file_path)



def collect_files(src_dir: str, dst_dir: str) -> None:
    for item in os.listdir(src_dir):
        item_path = os.path.join(src_dir, item)

        if os.path.isdir(item_path):
            collect_files(item_path, dst_dir)
        elif os.path.isfile(item_path):
            end_path = os.path.join(dst_dir, item)
            end_path = unique_filename(end_path)
            shutil.copy2(item_path, end_path)


if __name__ == "__main__":

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]
    max_depth = None

    if len(sys.argv) > 2:
        max_depth = int(sys.argv[3])

    if max_depth is not None:
        collect_files_with_depth(input_dir, output_dir, max_depth)
    else:
        collect_files(input_dir, output_dir)
