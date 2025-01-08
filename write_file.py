import os

def write_file(relative_path: str, content: str) -> str:
    """Writes content to a file at the specified relative path.
    Creates a new file if one doesn't exist, overwrites existing files.
    Returns a confirmation message or an error message."""
    try:
        full_path = os.path.abspath(relative_path)  # convert relative path to absolute, for safety
        # Create necessary directories
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
        return f"Successfully wrote content to {relative_path}"
    except Exception as e:
        return f"Error writing to file: {e}"
