import os
from pathlib import Path
import logging

# Set up logging format
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

# Project name
project_name = "cnnClassifier"

# List of all files and folders to create
list_of_files = [
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "dvc.yaml",
    "params.yaml",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb",
    "templates/index.html"
]

# Create files and directories
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir = filepath.parent

    if not filedir.exists():
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Created directory: {filedir}")

    if not filepath.exists():
        with open(filepath, "w") as f:
            pass  # create empty file
        logging.info(f"Created empty file: {filepath}")
    else:
        logging.info(f"File already exists: {filepath}")
