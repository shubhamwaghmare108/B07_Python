"""
Enhanced logg.py - Standard Logging Example
=============================================

This demonstrates basic to intermediate logging using Python's built-in logging module.

Key Concepts:
- basicConfig() for quick setup
- Logging to a file
- Format string with detailed context
- Exception logging with traceback
"""

import logging

# Create a logger for this module
# __name__ gives us the module path (useful in larger projects)
logger = logging.getLogger("my_logger")

# Configure logging with basicConfig (one-time setup)
# Note: basicConfig only works once; subsequent calls are ignored
logging.basicConfig(
    level=logging.ERROR,                    # Minimum level to log
    filename='app1.log',                    # File to write to
    filemode='a',                           # 'a' = append, 'w' = overwrite
    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s '
           'module:(%(module)s) - function %(funcName)s:LineNo.%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'            # Optional: custom date format
)

def division(a, b):
    """
    Divide two numbers with logging.
    
    Args:
        a: Dividend
        b: Divisor
    
    Returns:
        float: Result of division
    
    Raises:
        ZeroDivisionError: If b is 0
    """
    logger.debug(f"Dividing {a} by {b}")
    c = a / b
    return c


# Test the logger with exception handling
if __name__ == "__main__":
    # Test 1: Normal operation (would work)
    # division(10, 2)  # Result: 5.0
    
    # Test 2: Exception case
    try:
        division(10, 0)  # This will raise ZeroDivisionError
    except ZeroDivisionError as e:
        # Option 1: logger.debug() - good for development
        logger.debug(f"Error occurred while dividing: {e}")
        
        # Option 2: logger.exception() - includes full traceback automatically
        # This is the preferred way to log exceptions
        logger.exception(f"Error occurred: {e}")
        logger.error(f"Error occurred: {e}", exc_info=True)  # Also log as error level without traceback
    
    # Test 3: Informational logs
    logger.info("Division completed successfully.")
    
    # Test 4: Warning level
    logger.warning("This is a warning message.")
    
    # Test 5: Error level (not an exception, just an error state)
    logger.error("This is an error message.")
    
    # Test 6: Critical level
    logger.critical("This is a critical message.")

"""
Expected log output (app1.log):

2024-12-15 10:30:45 - my_logger - DEBUG - logg.py module:(logg) - function division:LineNo.21 - Dividing 10 by 0
2024-12-15 10:30:45 - my_logger - DEBUG - logg.py module:(logg) - function <module>:LineNo.45 - Error occurred while dividing: division by zero
2024-12-15 10:30:45 - my_logger - ERROR - logg.py module:(logg) - function <module>:LineNo.48 - Error occurred: division by zero
Traceback (most recent call last):
  File "logg.py", line 41, in <module>
    division(10, 0)
  File "logg.py", line 21, in division
    c = a / b
ZeroDivisionError: division by zero
2024-12-15 10:30:45 - my_logger - INFO - logg.py module:(logg) - function <module>:LineNo.51 - Division completed successfully.
2024-12-15 10:30:45 - my_logger - WARNING - logg.py module:(logg) - function <module>:LineNo.54 - This is a warning message.
2024-12-15 10:30:45 - my_logger - ERROR - logg.py module:(logg) - function <module>:LineNo.57 - This is an error message.
2024-12-15 10:30:45 - my_logger - CRITICAL - logg.py module:(logg) - function <module>:LineNo.60 - This is a critical message.

BEST PRACTICES DEMONSTRATED:
1. ✓ Use __name__ for logger identification
2. ✓ Configure once with basicConfig
3. ✓ Use logger.exception() for exceptions (includes traceback)
4. ✓ Use appropriate log levels
5. ✓ Include context in log messages

IMPROVEMENTS FOR PRODUCTION:
- Use logging.handlers.RotatingFileHandler to limit log file size
- Use different handlers for different levels (file for all, console for INFO+)
- Consider json logger for machine parsing
- Don't log sensitive information (passwords, tokens, PII)
"""
