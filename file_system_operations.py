"""File System Operations API."""

import os
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
        os.makedirs(relative_path, exist_ok=True)
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
        if os.path.exists(relative_path):
            os.remove(relative_path)
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
        shutil.move(source_path, destination_path)
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
        if os.path.isdir(source_path):
            shutil.copytree(source_path, destination_path)
        else:
            shutil.copy2(source_path, destination_path)  # copy2 preserves metadata
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
        if os.path.exists(code):
            try:
                # Attempt to execute the file as a Python script
                with open(code, "r") as f:
                    exec(f.read())  # Use exec for file execution
                return {"output": "", "status": "success"} # Return success if execution completes without error
            except Exception as e:
                return {"status": "failed", "message": str(e)}
        else:
            try:
                # Attempt to execute the string as Python code
                exec(code)
                return {"output": "", "status": "success"} # Return success if execution completes without error
            except Exception as e:
                return {"status": "failed", "message": str(e)}
    except Exception as e:
        return {"status": "failed", "message": str(e)}

