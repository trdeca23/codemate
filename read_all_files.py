import os
from typing import List, Dict, Union
from config import TARGET_DIR

def read_all_files(exclude: List[str] = None, path_filter: str = None) -> Dict[str, Union[str, Exception]]:
    """
    Reads the contents of all files under the TARGET_DIR, optionally filtering by path_filter and excluding specific files/directories.

    Args:
        exclude (list, optional): A list of subdirectories, files, or extensions to ignore. Defaults to None.
        path_filter (str, optional): A string to filter files by. Only files containing this string in their path will be read. Defaults to None.    

    Returns:
        dict: A dictionary where keys are relative file paths and values are either file contents (str) or exceptions (Exception) encountered while reading.
    """

    results = {}
    exclude = exclude or []
    for root, _, files in os.walk(TARGET_DIR):
        rel_root = os.path.relpath(root, TARGET_DIR)
        for file in files:

            rel_path = os.path.join(rel_root, file)
            if any(ex in file or ex in rel_root for ex in exclude):
                continue  # Skip excluded files/directories

            if path_filter and path_filter not in rel_path:
                continue  # Skip files that don't match the filter

            try:
                with open(os.path.join(TARGET_DIR, rel_path), 'r') as f:
                    content = f.read()
                    results[rel_path] = content

            except FileNotFoundError:
                results[rel_path] = FileNotFoundError(f"File not found: {rel_path}")
            except PermissionError:
                results[rel_path] = PermissionError(f"Permission denied: {rel_path}")
            except Exception as e:
                return e
    return results