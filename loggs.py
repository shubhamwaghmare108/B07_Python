
import logging
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s|%(levelno)d -%(name)s - %(module)s|%(pathname)s - %(funcName)s-(line no: %(lineno)d) - %(message)s',
                    datefmt = '%A-%y-%B %Z-%z:%H:%M:%S %p')

logger.info("This is an info message")

def add_numbers(a, b):
    logging.debug(f"Adding {a} and {b}")
    return a + b

result = add_numbers(5, 3)
logging.info(f"Result of addition: {result}")

logging.warning("This is a warning message")
logging.error("This is an error message")
logging.critical("This is a critical message")