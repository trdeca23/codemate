"""File System Operations API."""

import os
from pathlib import Path
from config import TARGET_DIR
import shutil

def make_directory(relative_path: str) -> dict:
    """Creates a new directory at the specified relative path.

    Args:
        relative_path (str): The relative path to the directory to create.

    Returns:
        dict: A dictionary indicating success or failure, along with any error messages.
              {"status": "success"} or {"status": "failed", "message": "error message"}
    """

    try:
        dir_path = TARGET_DIR / relative_path
        if not dir_path.is_relative_to(TARGET_DIR):
            raise RuntimeError(f"Access denied. Path outside TARGET_PATH: {dir_path}")
        os.makedirs(dir_path, exist_ok=True)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failed", "message": str(e)}


def delete_file(relative_path: str) -> dict:
    """Deletes the file at the specified relative path.

    Args:
        relative_path (str): The relative path to the file to delete.

    Returns:
        dict: A dictionary indicating success or failure, along with any error messages.
    """
    try:
        file_path = TARGET_DIR / relative_path
        if not file_path.is_relative_to(TARGET_DIR):
            raise RuntimeError(f"Access denied. Path outside TARGET_PATH: {file_path}")
        if file_path.exists():
            os.remove(file_path)
            return {"status": "success"}
        else:
            return {"status": "failed", "message": f"File not found: {relative_path}"}
    except Exception as e:
        return {"status": "failed", "message": str(e)}


def move_file(source_path: str, destination_path: str) -> dict:
    """Moves a file or directory from the source path to the destination path.

    Args:
        source_path (str): The relative path to the source file or directory.
        destination_path (str): The relative path to the destination.

    Returns:
        dict: A dictionary indicating success or failure, along with any error messages.
    """
    try:
        source_path_abs = TARGET_DIR / source_path
        destination_path_abs = TARGET_DIR / destination_path
        if not source_path_abs.is_relative_to(TARGET_DIR) or not destination_path_abs.is_relative_to(TARGET_DIR):
            raise RuntimeError(f"Access denied. Source or destination path outside TARGET_PATH.")
        shutil.move(source_path_abs, destination_path_abs)
        return {"status": "success"}
    except Exception as e:
        return {"status": "failed", "message": str(e)}


def copy_file(source_path: str, destination_path: str) -> dict:
    """Copies a file or directory from the source to the destination.

    Args:
        source_path (str): The relative path to the source file or directory.
        destination_path (str): The relative path to the destination.

    Returns:
         dict: A dictionary indicating success or failure, along with any error messages.
    """
    try:
        source_path_abs = TARGET_DIR / source_path
        destination_path_abs = TARGET_DIR / destination_path
        if not source_path_abs.is_relative_to(TARGET_DIR) or not destination_path_abs.is_relative_to(TARGET_DIR):
            raise RuntimeError(f"Access denied. Source or destination path outside TARGET_PATH.")      

        if source_path_abs.is_dir():
            shutil.copytree(source_path_abs, destination_path_abs)
        else:
            shutil.copy2(source_path_abs, destination_path_abs)  # copy2 preserves metadata
        return {"status": "success"}
    except Exception as e:
        return {"status": "failed", "message": str(e)}


def local_code_execution(code: str) -> dict:
    """Runs code for testing purposes.

    Args:
        code (str): Either a path to a Python file or a string of Python code.

    Returns:
        dict: A dictionary containing the output of the code execution or an error message.
    """

    try:
        code_path = TARGET_DIR / code
        if code_path.exists():
            try:
                # Attempt to execute the file as a Python script
                if not code_path.is_relative_to(TARGET_DIR):
                    raise RuntimeError(f"Access denied. Code path outside TARGET_PATH: {code_path}")   
                with open(code_path, "r") as f:
                    exec(f.read())  # Use exec for file execution
                return {"output": "", "status": "success"} # Return success if execution completes without error
            except Exception as e:
                return {"status": "failed", "message": str(e)}
        else:
            try:
                exec(code) # Attempt to execute the string as Python code
                return {"output": "", "status": "success"} # Return success if execution completes without error
            except Exception as e:
                return {"status": "failed", "message": str(e)}
    except Exception as e:
        return {"status": "failed", "message": str(e)}
