import os
from typing import List, Dict, Union
from utils.config import TARGET_DIR

def get_structure_in_target_dir(exclude: List[str] = None, recursive: bool = True) -> Union[Dict[str, Union[List[Dict], Exception]], Exception]:
    """
    Returns a dictionary representing the directory structure under TARGET_DIR.

    Args:
        exclude (list, optional): A list of subdirectories, files, or extensions to ignore. Defaults to None.
        recursive (bool, optional): Whether to recurse into subdirectories. Defaults to True.

    Returns:
        dict: A dictionary where keys are relative paths and values are lists of dictionaries containing filename and size.
             Or, returns an Exception if an error occurs.
    """

    try:
        dir_structure = {}
        exclude = exclude or []

        if recursive:
            for root, _, files in os.walk(TARGET_DIR):
                rel_root = os.path.relpath(root, TARGET_DIR)  # Make relative to TARGET_DIR
                file_list = []

                if any(ex in rel_root for ex in exclude): #Exclude directories
                    continue

                for file in files:
                    if any(ex in file for ex in exclude): #Exclude files
                        continue

                    file_path = os.path.join(root, file)
                    try:
                        file_size = os.path.getsize(file_path)
                        file_list.append({"filename": file, "size": file_size})

                    except Exception as inner_e: #e.g., if there was an issue determining the file size
                        file_list.append({"filename": file, "error": inner_e})

                dir_structure[rel_root] = file_list


        else:  # Non-recursive, only list the top-level directory
            for entry in os.listdir(TARGET_DIR):
                if any(ex in entry for ex in exclude):
                    continue

                entry_path = os.path.join(TARGET_DIR, entry)

                if os.path.isfile(entry_path):
                    try:
                      file_size = os.path.getsize(entry_path)
                      dir_structure[entry] = {"filename": entry, "size": file_size}
                    except Exception as inner_e:
                        dir_structure[entry] = {"filename": entry, "error": inner_e}
                elif os.path.isdir(entry_path):
                    dir_structure[entry] = {"filename": entry, "size": 0} #Assign size zero for now

        return dir_structure


    except PermissionError:
        return PermissionError(f"Permission denied accessing TARGET_DIR")
    except Exception as e:
        return e
