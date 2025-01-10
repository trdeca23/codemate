import os
import json
from typing import List, Dict, Union
from utils.config import TARGET_DIR

if TARGET_DIR is None:
    raise EnvironmentError("TARGET_DIR environment variable not set.")

DEF_EXCLUDE = ['.git', '.venv', '__pycache__', '.DS_Store', '.jpg', '.png', '.pyc', '.env', 'interaction_log.txt']

def read_all_files_in_target_dir(exclude: List[str] = DEF_EXCLUDE, path_filter: str = None) -> Dict[str, Union[str, Exception, bytes]]:
    """Reads the contents of all files under TARGET_DIR, handling potential UnicodeDecodeErrors and other exceptions.
       Prioritizes decoding as UTF-8 but falls back to storing raw bytes if decoding fails.

    Args:
        exclude: A list of subdirectories, files, or extensions to ignore. Defaults to ['.git', '.venv', '__pycache__', '.DS_Store', '.jpg', '.png', '.pyc', '.env', 'interaction_log.txt'].
        path_filter: A string to filter files by.

    Returns:
        A dictionary where keys are relative file paths and values are either
        file contents (str if decodable, bytes otherwise) or exceptions.

    Raises:
        EnvironmentError: If TARGET_DIR is not defined in environment variables.
    """


    results = {}
    exclude = exclude or []


    for root, _, files in os.walk(TARGET_DIR):
        rel_root = os.path.relpath(root, TARGET_DIR)

        if any(ex in rel_root for ex in exclude):
            continue

        for file in files:
            rel_path = os.path.join(rel_root, file)

            if any(ex in file or ex in rel_root for ex in exclude):
                continue
            if path_filter and path_filter not in rel_path:
                continue

            full_path = os.path.join(TARGET_DIR, rel_path)
            try:
                with open(full_path, 'rb') as f:
                    content = f.read()
                    try:
                         results[rel_path] = content.decode('utf-8')
                    except UnicodeDecodeError:
                        results[rel_path] = content  # Store raw bytes if decoding fails

            except (FileNotFoundError, PermissionError, OSError) as e:  # Handle OS-level errors too
                results[rel_path] = e
            except Exception as e:  # Catch any other unexpected exceptions
                results[rel_path] = e



    return results


if __name__ == "__main__":
    # Example usage (set TARGET_DIR in your environment):
    outfile = "codemate_output.txt"
    # os.environ["TARGET_DIR"] = "/path/to/your/target/dir"  # Replace with your actual path. Do this outside of the function and before calling
    file_content = read_all_files_in_target_dir(exclude=['.git', '.venv', '__pycache__', '.DS_Store', '.jpg', '.png', '.pyc', '.env', 'interaction_log.txt', outfile])  #, path_filter='.py')
    # print(json.dumps(file_content, indent=4, default=str))
    with open(outfile, "w+") as text_file:
        for file in file_content:
            text_file.write(f"Filename: {file}\n")
            text_file.write(str(file_content[file]))
            text_file.write('\n----------------END OF FILE----------------\n\n\n')
