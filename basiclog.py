import logging


logger = logging.getLogger("my_logger")

logger.setLevel(logging.DEBUG)  # Set the logger to capture all levels of logs

name = 'shubham'
logger.debug("This is a debug message") #10
logger.info(f"User: {name} has logged in") #20
#logger.warning("This is a warning message") #30
#logger.error("This is an error message") #40
#logger.critical("This is a critical message") #50
