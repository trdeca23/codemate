import os
from typing import List, Dict, Union

def read_all_files(target_path: str = ".", exclude: List[str] = None, path_filter: str = None) -> Dict[str, Union[str, Exception]]:
    """
    Reads the contents of all files under target_path, optionally filtering by path_filter and excluding specific files/directories.

    Args:
        target_path (str): The path to the target directory. Defaults to the current directory.
        exclude (list, optional): A list of subdirectories, files, or extensions to ignore. Defaults to None.
        path_filter (str, optional): A string to filter files by. Only files containing this string in their path will be read. Defaults to None.    

    Returns:
        dict: A dictionary where keys are relative file paths and values are either file contents (str) or exceptions (Exception) encountered while reading.
    """

    results = {}
    exclude = exclude or []
    for root, _, files in os.walk(target_path):
        rel_root = os.path.relpath(root, target_path)
        for file in files:

            rel_path = os.path.join(rel_root, file)
            if any(ex in file or ex in rel_root for ex in exclude):
                continue  # Skip excluded files/directories

            if path_filter and path_filter not in rel_path:
                continue  # Skip files that don't match the filter

            try:
                with open(os.path.join(target_path, rel_path), 'r') as f:
                    content = f.read()
                    results[rel_path] = content

            except FileNotFoundError:
                results[rel_path] = FileNotFoundError(f"File not found: {rel_path}")
            except PermissionError:
                results[rel_path] = PermissionError(f"Permission denied: {rel_path}")
            except Exception as e:

    return results