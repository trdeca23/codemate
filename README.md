# Gemini File Utilities Library

This library provides a set of file and directory manipulation functions designed to be used as tools within the Gemini Generative AI Python SDK. It 
facilitates leveraging function calling within Gemini, enabling low-code/no-code interactions with the AI model for various file-related tasks.  This allows for human-in-the-loop AI programming, where Gemini can execute code locally to interact with the file system based on user instructions or its own reasoning.


## Recommended Usage with Version Control

For robust and secure development using this library with Gemini, it's highly recommended to use a version control system like Git.  This enables you to track changes, review AI-generated code modifications before they are applied, and maintain a history of your project's evolution.  This iterative process, where a human reviews and approves or rejects changes suggested by the AI, is crucial for safe and reliable low-code AI development.  This is especially true for functions which modify the files, and the iterative process of making changes to files via this library should be accompanied by corresponding commits.


## Available Functions

*   **`get_dir_structure(target_path: str = ".", exclude: List[str] = None, recursive: bool = True)`:** Returns a dictionary representing the directory structure under the given path. Includes file sizes and allows for excluding specific files/directories and recursive or non-recursive traversal. 

*   **`read_file(relative_path: str)`:** Reads and returns the contents of a file at the specified relative path.

*   **`read_all_files(target_path: str = ".", exclude: List[str] = None, path_filter: str = None)`:** Reads the contents of all files within the target directory (and optionally subdirectories) that match a given filter, while also allowing exclusion of specified files/directories. Returns a dictionary mapping filenames to contents or errors.

*   **`write_file(relative_path: str, content: str, overwrite: bool = True)`:** Writes content to a file at the specified relative path, optionally overwriting the file if it exists. Creates necessary parent directories.

*   **(Suggested) `list_directory(relative_path: str = None)`:** Lists all files and directories at a specified relative path (if given, otherwise list files in current directory).
*   **(Suggested) `make_directory(relative_path: str)`:** Creates a new directory at the specified relative path.

*   **(Suggested) `delete_file(relative_path: str)`:** Deletes a file at the specified relative path.

*   **(Suggested) `move_file(source_path: str, destination_path: str)`:** Moves a file or directory from source to destination.

*   **(Suggested) `copy_file(source_path: str, destination_path: str)`:** Copies a file or directory from source to destination.


## Usage with Gemini

These functions are designed to be used as tools within the Gemini `GenerativeModel` framework. By passing these functions as tools, you empower Gemini to interact directly with the file system: reading file contents, writing to files, creating directories, listing directory contents and more, all based on conversation and instructions or its own autonomous decisions.

This library streamlines the process of creating complex, file-driven workflows within Gemini, providing a powerful and flexible approach to low-code/no-code AI programming.  The additional suggested tools would further enhance Gemini's file system manipulation abilities, enabling greater automation within your workflows.


## Security and the TARGET_PATH Environment Variable

For security reasons, all file operations are restricted to a specific target directory.  This target directory is specified using the `TARGET_PATH` 
environment variable.  **You MUST set this environment variable before using any functions in this library.**  You have several options for setting environment variables:

**1. Using the .env file:**

Create a `.env` file in the root directory of your project and add the following lines:

```
TARGET_PATH=/path/to/your/target/directory  # Replace with your desired directory
API_KEY=YOUR_ACTUAL_API_KEY
```

In your Python script, these are automatically loaded the from the `.env` file:

```python
from dotenv import load_dotenv
load_dotenv()

# Access the variables:
target_path = os.environ.get("TARGET_PATH")
api_key = os.environ.get("API_KEY")
```

**2. Exporting directly (Bash/Zsh):**

```bash
export TARGET_PATH="/path/to/your/target/directory"  # Replace with your desired directory
export API_KEY="YOUR_ACTUAL_API_KEY"
```

**3. Setting directly (Windows Command Prompt):**

```cmd
set TARGET_PATH=C:\path\to\your\target\directory
set API_KEY=YOUR_ACTUAL_API_KEY
```


**Important Security Notes:**

*   The library uses `pathlib` and resolves `TARGET_PATH` to its absolute path to prevent directory traversal attacks.
*   All functions that modify the file system (e.g., `write_file`, `delete_file`) include checks to ensure that operations occur *only* within the `TARGET_PATH` directory. Attempts to access files or directories outside this path will result in a `RuntimeError`.  This safeguards against unintended file system modifications.
*   It's strongly recommended to set `TARGET_PATH` to a dedicated directory specifically for use with Gemini and this library to further enhance security.
