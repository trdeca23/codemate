import os
from typing import Union
from config import TARGET_DIR

def write_file(relative_path: str, content: str, overwrite: bool = True) -> Union[str, Exception]:
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

        # Check if the file_path is within the TARGET_DIR
        if not file_path.is_relative_to(TARGET_DIR):  # Enforce security
            raise RuntimeError(f"Access denied. Path outside TARGET_PATH: {file_path}")
        
        # Create parent directories if they don't exist:
        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)

        if os.path.exists(file_path) and not overwrite:

            with open(file_path, 'w') as f:
                f.write(content)

            return "File written successfully."

    except FileExistsError as fee: #More specific exception handling
      return fee
    except Exception as e:
        return e
