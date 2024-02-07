import logging
from logging.handlers import RotatingFileHandler

# Set up logging
logger = logging.getLogger("custom_logger")
logger.setLevel(logging.DEBUG)

# Create a rotating file handler
log_file = "custom_log.log"
handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024, backupCount=5)
handler.setLevel(logging.DEBUG)

# Create a formatter and set the formatter for the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)