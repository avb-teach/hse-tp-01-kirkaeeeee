import os
import shutil
import sys


def unique_filename(path):
    base, ext = os.path.splitext(path)
    duplicates = 1
    new_path = path
    while os.path.exists(new_path):
        new_path = f"{base}{duplicates}{ext}"
        duplicates += 1
    return new_path


def collect_files_with_depth(input_dir, output_dir, d):
    for root, dirs, files in os.walk(input_dir):
        depth = root[len(input_dir):].count(os.sep) + 1
        
        if depth <= max_depth:
            relative_path = os.path.relpath(root, input_dir)
            end_dir = os.path.join(output_dir, relative_path)
            
            if not os.path.exists(end_dir):
                os.makedirs(end_dir)

            for file in files:
                source_file = os.path.join(root, file)
                end_file = os.path.join(end_dir, file)
                shutil.copy2(source_file, end_file)
        else:
            relative_path = os.path.relpath(root, input_dir)
            output_dir2 = os.path.join(output_dir, *relative_path.split(os.sep)[max_depth-1:])
            
            if not os.path.exists(output_dir2):
                os.makedirs(output_dir2)

            for f1 in files:
                source_file = os.path.join(root, f1)
                end_file = os.path.join(output_dir2, f1)
                shutil.copy2(source_file, end_file)


def collect_files(input_dir, output_dir):
    for item in os.listdir(input_dir):
        item_path = os.path.join(input_dir, item)

        if os.path.isdir(item_path):
            collect_files(item_path, output_dir)
        elif os.path.isfile(item_path):
            end_path = os.path.join(output_dir, item)
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
