#import logging
import logging

# Create a logger
logger = logging.getLogger("my_logger")

# Configure logging to write to a file with a specific format
logging.basicConfig(level=logging.DEBUG,
                    #filename='app1.log',
                    #filemode='w',
                    format='%(asctime)s - %(name)s - %(levelname)s|%(levelno)d - %(filename)s '
                    'module:(%(module)s) - function %(funcName)s:LineNo.%(lineno)d - %(message)s - %(thread)d - %(threadName)s - %(process)d - %(processName)s',
                    datefmt='%Y/%B/%d %H:%M:%S')



def division(a, b):
    logger.debug(f"Dividing {a} by {b}")
    c = a / b
    logger.info(f"Result of division: {c}")
    return c
    

# Test the logger
try:
    division(10, 0)  # This will raise a ZeroDivisionError and log the error
except ZeroDivisionError as e:
    logger.debug(f"Error occurred while dividing: {e}")
    #logger.exception(f"Error occurred: {e}, Traceback info: {e.__traceback__}, Traceback details: {e.__traceback__.tb_frame.f_globals}")
    
logger.info("Division completed successfully.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")
