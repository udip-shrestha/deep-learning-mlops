import os
import sys
import logging

# Define log format
LOG_FORMAT = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

# Log file path
LOG_DIR = "logs"
LOG_FILE_PATH = os.path.join(LOG_DIR, "running_logs.log")
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler(sys.stdout),
    ]
)

# Named logger for cnnClassifier
logger = logging.getLogger("cnnClassifierLogger")
