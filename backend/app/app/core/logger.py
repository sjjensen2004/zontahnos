import logging
import sys

# Define log format (includes module name)
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

# Create a custom logging filter to exclude Rx logs
class ExcludeRxFilter(logging.Filter):
    def filter(self, record):
        return not record.name.startswith("Rx")

# Create a root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Apply the custom filter to the console handler
console_handler.addFilter(ExcludeRxFilter())

# Add the console handler to the root logger
root_logger.addHandler(console_handler)

# Create a file handler for Rx logs
rx_file_handler = logging.FileHandler("rx_logs.log")
rx_file_handler.setLevel(logging.DEBUG)
rx_file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Create a logger for Rx and add the file handler
rx_logger = logging.getLogger("Rx")
rx_logger.setLevel(logging.DEBUG)
rx_logger.addHandler(rx_file_handler)

# Function to get logger for each module
def get_logger(module_name: str):
    return logging.getLogger(module_name)