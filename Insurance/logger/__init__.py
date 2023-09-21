# importing libraries
import logging
from datetime import datetime
import os

# Creating logs directory to store log in files
LOG_DIR = "insurance_log"

# Creating file name for log file based on current timestamp
CURRENT_TIME_STAMP = f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

# define the path to store log with folder_name
LOG_FILE_NAME = f"log_{CURRENT_TIME_STAMP}.log"

# create one if directory does not exists
os.makedirs(LOG_DIR, exist_ok=True)

# log file path
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

# log basic config file name format
logging.basicConfig(
    filename=LOG_FILE_PATH,
    filemode="w",
    format="[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)
