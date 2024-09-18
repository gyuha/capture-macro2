import platform


def is_macos() -> bool:
    """
    is_macos returns True if the current platform is macOS.
    """
    return platform.system() == "Darwin"


def is_windows() -> bool:
    """
    is_windows returns True if the current platform is Windows.
    """
    return platform.system() == "Windows"


if __name__ == "__main__":
    print(f"macOS: {is_macos()}")
    print(f"Windows: {is_windows()}")