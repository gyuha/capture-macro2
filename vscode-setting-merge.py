import json
import os
import platform
import sys


def merge_json_files(common_file, os_specific_file):
    data = {}
    # Load common settings
    if os.path.exists(common_file):
        with open(common_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    # Load OS-specific settings and merge
    if os.path.exists(os_specific_file):
        with open(os_specific_file, "r", encoding="utf-8") as f:
            os_data = json.load(f)
            data.update(os_data)
    return data


def save_json_file(data, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    # Detect the current operating system
    current_os = platform.system()
    if current_os == "Darwin":
        os_folder = "mac"
    elif current_os == "Windows":
        os_folder = "windows"
    else:
        print(f"Unsupported operating system: {current_os}")
        sys.exit(1)

    # Define file paths
    vscode_dir = ".vscode"
    common_dir = os.path.join(vscode_dir, "common")
    os_dir = os.path.join(vscode_dir, os_folder)

    # Files to process
    files = ["settings.json", "launch.json"]

    # Process each file
    for filename in files:
        common_file = os.path.join(common_dir, filename)
        os_specific_file = os.path.join(os_dir, filename)
        output_file = os.path.join(vscode_dir, filename)

        merged_data = merge_json_files(common_file, os_specific_file)
        save_json_file(merged_data, output_file)
        print(f"Merged {filename} for {current_os} into {output_file}")


if __name__ == "__main__":
    main()
