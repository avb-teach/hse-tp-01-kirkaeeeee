import os
import shutil
import sys

log_file_path = "collect_files.log"


def log(message):
    print(message)
    with open(log_file_path, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def get_unique_filename(path):
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
        log(f"depth {depth}")
        
        if depth <= d:
            relative_path = os.path.relpath(root, input_dir)
            destination_dir = os.path.join(output_dir, relative_path)
            log(f"1. depth {depth}: relative_path={relative_path}, destination_dir={destination_dir}")

            if not os.path.exists(destination_dir):
                log(f"1. depth {depth}: makedirs({destination_dir})")
                os.makedirs(destination_dir)

            for file in files:
                source_file = os.path.join(root, file)
                destination_file = os.path.join(destination_dir, file)
                log(f"1. depth {depth}: copy2({source_file} to {destination_file})")
                shutil.copy2(source_file, destination_file)
        else:
            relative_path = os.path.relpath(root, input_dir)
            new_output_dir = os.path.join(output_dir, *relative_path.split(os.sep)[d-1:])
            
            if not os.path.exists(new_output_dir):
                log(f"2. depth {depth}: makedirs({new_output_dir})")
                os.makedirs(new_output_dir)

            for file in files:
                source_file = os.path.join(root, file)
                destination_file = os.path.join(new_output_dir, file)
                log(f"2. depth {depth}: copy2({source_file} to {destination_file})")
                shutil.copy2(source_file, destination_file)


def collect_files(input_dir, output_dir):
    for item in os.listdir(input_dir):
        item_path = os.path.join(input_dir, item)

        if os.path.isdir(item_path):
            collect_files(item_path, output_dir)
        elif os.path.isfile(item_path):
            destination_path = os.path.join(output_dir, item)
            destination_path = get_unique_filename(destination_path)
            shutil.copy2(item_path, destination_path)


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
