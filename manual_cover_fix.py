import os
import sys
import subprocess
import time


def check_for_cover(folder):
    """
    Check if 'cover.jpg' exists in the specified folder.
    """
    files_lower = [file.lower() for file in os.listdir(folder)]
    return 'cover.jpg' in files_lower


def open_folders_from_file(file_path, unresolved_output_file):
    """
    Open unresolved folders one by one and automatically check for cover files.

    Parameters:
    - file_path (str): Path to the file containing unresolved folders.
    - unresolved_output_file (str): Path to the output file for unresolved folders.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    with open(file_path, 'r') as f:
        folders = [line.strip() for line in f if line.strip()]

    unresolved_folders = []

    for folder in folders:
        if not os.path.isdir(folder):
            print(f"Folder does not exist: {folder}")
            unresolved_folders.append(folder)
            continue

        print(f"Checking folder: {folder}")
        # Open folder in the system's file explorer
        if os.name == 'nt':  # Windows
            subprocess.Popen(f'explorer "{folder}"')
        elif os.name == 'posix':  # macOS/Linux
            subprocess.Popen(
                ['open' if sys.platform == 'darwin' else 'xdg-open', folder])

        # Wait for the user to make changes and check for cover files
        while True:
            time.sleep(2)  # Wait for 5 seconds before checking
            if check_for_cover(folder):
                print(f"'cover.jpg' or 'cover.png' found in: {folder}")
                break
            else:
                print(f"No cover file found in: {folder}. Please add it.")

        # Recheck for cover after the wait loop
        if not check_for_cover(folder):
            print(f"Unresolved: {folder}")
            unresolved_folders.append(folder)

    # Write unresolved folders back to the output file
    with open(unresolved_output_file, 'w') as f:
        for folder in unresolved_folders:
            f.write(folder + '\n')

    print(f"\nUnresolved folders written to: {unresolved_output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python open_folders.py <unresolved_folders_file> <unresolved_output_file>")
        sys.exit(1)

    unresolved_file = sys.argv[1]
    unresolved_output_file = sys.argv[2]

    open_folders_from_file(unresolved_file, unresolved_output_file)
