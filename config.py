import os
import pathlib
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
TARGET_PATH = os.environ.get("TARGET_PATH")
if TARGET_PATH is None:
    raise EnvironmentError("TARGET_PATH environment variable must be set.")

TARGET_DIR = pathlib.Path(TARGET_PATH).resolve()
