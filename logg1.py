import logging
from logging.handlers import SMTPHandler

# Create logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - '
    'function %(funcName)s:LineNo.%(lineno)d - %(message)s'
)

# File Handler
file_handler = logging.FileHandler('app2.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Console Handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

# Email Handler
email_handler = SMTPHandler(
    mailhost=('smtp.gmail.com', 587),
    fromaddr='scwagh123@gmail.com',
    toaddrs=['scwagh123@gmail.com'],
    subject='Application Error',
    credentials=('scwagh123@gmail.com', 'knnoetbxndabypdy'),
    secure=()
)

email_handler.setLevel(logging.ERROR)
email_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.addHandler(email_handler)

# Test logs
logger.debug("This is a debug message.")
logger.info("This is an info message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")