import os
from utils.config import TARGET_DIR

def read_file_in_target_dir(relative_path: str) -> str:
    """
    Returns a string containing the contents of the file at the specified relative_path.
    Args:
        relative_path (str): The relative path to the file.

    Returns:
        str: The content of the file.
             Returns an error message string if there's an issue.
    """
    try:
        file_path = TARGET_DIR / relative_path  # Use pathlib for safe path joining

        # Check if the file_path is within the TARGET_DIR
        if not file_path.is_relative_to(TARGET_DIR):  # Enforce security
            raise RuntimeError(f"Access denied. Path outside TARGET_PATH: {file_path}")
        with open(file_path, 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"Error: File not found at {file_path}"
    except Exception as e:
        return f"Error reading file: {e}"
