import os

def read_file(relative_path: str) -> str:
    """
    Returns a string containing the contents of the file at the specified relative_path.
    Args:
        relative_path (str): The relative path to the file.

    Returns:
        str: The content of the file.
             Returns an error message string if there's an issue.
    """
    try:
        with open(relative_path, 'r') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"Error: File not found at {relative_path}"
    except Exception as e:
        return f"Error reading file: {e}"
