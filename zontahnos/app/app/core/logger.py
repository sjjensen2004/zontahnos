import logging
import sys

# Define log format (includes module name)
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

# Create a root logger
logging.basicConfig(
    level=logging.DEBUG,  # Default log level
    format=LOG_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout),  # Log to console
    ],
)

# Function to get logger for each module
def get_logger(module_name: str):
    # logging.getLogger("Rx").setLevel(logging.WARNING)
    return logging.getLogger(module_name)