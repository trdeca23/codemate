import os
from typing import List

def get_dir_structure(target_path: str=".", exclude: List[str]=None) -> str:  # TODO: change typing to exclude:[List[str], None]
    """
    Returns a dictionary representing the directory structure under target_path.

    Args:
        target_path (str): The path to the target directory. Defaults to the current directory.
        exclude (list, optional): A list of subdirectories, files, or extensions to ignore. Defaults to None.

    Returns:
        dict: A dictionary where keys are relative paths and values are lists of filenames.
             Returns an error message string if there's an issue.
    """
    try:
        dir_structure = {}
        exclude = exclude or []  # Handle if exclude is None

        for root, _, files in os.walk(target_path):
            rel_path = os.path.relpath(root, target_path)
            filtered_files = []
            for file in files:
                if any(ex in file or ex in rel_path for ex in exclude):
                    continue  # Skip excluded files/directories
                filtered_files.append(file)
            if filtered_files:
                dir_structure[rel_path if rel_path != "." else ""] = filtered_files

        return dir_structure

    except Exception as e:
        return f"Error: {e}"
