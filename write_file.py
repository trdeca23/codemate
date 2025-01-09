import os
from typing import Union
from config import TARGET_DIR

def write_file_in_target_dir(relative_path: str, content: str, overwrite: bool = True) -> Union[str, Exception]:
    """
    Writes content to a file at the specified relative path.

    Args:
        relative_path (str): The relative path to the file.
        content (str): The content to write to the file.
        overwrite (bool, optional): Whether to overwrite the file if it exists. Defaults to True. If false, and the file exists, raises FileExistsError.

    Returns:
         str: A success message.
         Exception: Exception if file writing fails.
    """
    try:

        file_path = TARGET_DIR / relative_path  # Use pathlib for safe path joining

        # Security check: Check if the file_path is within the TARGET_DIR
        if not file_path.is_relative_to(TARGET_DIR):  # Enforce security
            raise RuntimeError(f"Access denied. Path outside TARGET_PATH: {file_path}")
        
        # Create parent directories if they don't exist.
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Determine file write mode based on overwrite parameter.
        mode = 'w' if overwrite else 'x'  # 'x' will raise FileExistsError if the file already exists.

        with open(file_path, mode) as f:
            f.write(content)

        return "File written successfully."

    except FileExistsError as fee: #More specific exception handling
      return fee
    except Exception as e:
        return e
