import os
import sys
import json
import base64
import joblib
import yaml

from pathlib import Path
from typing import Any
from ensure import ensure_annotations
from box import ConfigBox
from box.exceptions import BoxValueError
from cnnClassifier import logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Read YAML file and return contents as ConfigBox (dot-accessible dict)."""
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file loaded successfully from: {path_to_yaml}")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError(f"YAML file is empty: {path_to_yaml}")
    except Exception as e:
        logger.error(f"Error reading YAML file: {e}")
        raise e

@ensure_annotations
def create_directories(paths: list, verbose: bool = True) -> type(None):
    """Create multiple directories from a list of Path objects."""
    for path in paths:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")




# @ensure_annotations
# def save_json(path: Path, data: dict) -> None:
#     """Save dictionary data to a JSON file."""
#     with open(path, "w") as f:
#         json.dump(data, f, indent=4)
#     logger.info(f"JSON file saved at: {path}")


# @ensure_annotations
def save_json(path: Path, data: dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"JSON file saved at: {path}")



@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Load JSON file and return contents as ConfigBox."""
    with open(path) as f:
        content = json.load(f)
    logger.info(f"JSON file loaded from: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path) -> None:
    """Save any object as a binary file using joblib."""
    joblib.dump(value=data, filename=path)
    logger.info(f"Binary file saved at: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """Load binary file using joblib."""
    data = joblib.load(path)
    logger.info(f"Binary file loaded from: {path}")
    return data


@ensure_annotations
def get_size(path: Path) -> str:
    """Return file size in KB."""
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"


@ensure_annotations
def decode_image(img_base64: str, file_path: Path) -> None:
    """Decode base64 string and save as an image file."""
    img_data = base64.b64decode(img_base64)
    with open(file_path, 'wb') as f:
        f.write(img_data)
    logger.info(f"Image decoded and saved at: {file_path}")


@ensure_annotations
def encode_image_to_base64(image_path: Path) -> str:
    """Read image file and encode it to base64 string."""
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    logger.info(f"Image encoded to base64 from: {image_path}")
    return encoded