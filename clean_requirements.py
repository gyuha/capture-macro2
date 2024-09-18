import os
import subprocess
import sys
import venv


def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, executable="/bin/bash")
    output, error = process.communicate()
    return output.decode("utf-8").strip()


def get_venv_pip():
    if hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix):
        # We're in a virtualenv
        return os.path.join(sys.prefix, "bin", "pip")
    else:
        # We're not in a virtualenv
        return "pip"


def get_installed_packages():
    pip_path = get_venv_pip()
    return set(run_command(f"{pip_path} freeze").split("\n"))


def get_used_packages():
    pip_path = get_venv_pip()
    run_command(f"{pip_path} install pipreqs")
    run_command("pipreqs . --force")
    with open("requirements.txt", "r") as f:
        return set(f.read().split("\n"))


def clean_requirements():
    pip_path = get_venv_pip()

    print("Checking if pipreqs is installed...")
    if run_command(f"{pip_path} show pipreqs").startswith("WARNING: Package(s) not found:"):
        print("pipreqs not found. Installing...")
        run_command(f"{pip_path} install pipreqs")

    print("Getting installed packages...")
    installed = get_installed_packages()

    print("Getting used packages...")
    used = get_used_packages()

    to_remove = installed - used

    if to_remove:
        print("Removing unused packages:")
        for package in to_remove:
            if package and not package.startswith("-e"):  # Avoid empty strings and editable packages
                print(f"Uninstalling {package}")
                run_command(f"{pip_path} uninstall -y {package}")
    else:
        print("No unused packages found.")

    print("Updating requirements.txt...")
    run_command(f"{pip_path} freeze > requirements.txt")

    print("Clean-up complete!")


if __name__ == "__main__":
    clean_requirements()
