"""
Enhanced logg1.py - Multiple Handlers Example
==============================================

This demonstrates advanced logging with multiple handlers:
- FileHandler: Captures all logs (DEBUG+)
- StreamHandler: Console output (INFO+)
- SMTPHandler: Email alerts (ERROR+)

Key Concepts:
- Logger vs Handlers vs Formatters
- Handler hierarchy and log routing
- Different levels per handler
- Real-world production setup
"""

import logging
from logging.handlers import SMTPHandler

# Create logger (central point for all logging)
logger = logging.getLogger("my_logger")

# Set the logger to capture DEBUG and above
# (handlers can be more restrictive)
logger.setLevel(logging.DEBUG)

# Create formatter (reusable for all handlers)
# Consistent format across all outputs
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - '
    'function %(funcName)s:LineNo.%(lineno)d - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# ============================================================================
# HANDLER 1: File Handler - Captures everything (DEBUG+)
# ============================================================================
# Use for: Persistent log storage for debugging and auditing
file_handler = logging.FileHandler('app2.log', mode='a')
file_handler.setLevel(logging.DEBUG)            # Capture all messages
file_handler.setFormatter(formatter)            # Apply format

# ============================================================================
# HANDLER 2: Stream Handler - Console output (INFO+)
# ============================================================================
# Use for: Development and monitoring - shows important info without noise
stream_handler = logging.StreamHandler()        # stdout by default
stream_handler.setLevel(logging.INFO)           # Skip DEBUG messages
stream_handler.setFormatter(formatter)

# ============================================================================
# HANDLER 3: Email Handler - Critical alerts (ERROR+)
# ============================================================================
# Use for: Immediate notification of serious issues to operations team
# 
# SECURITY WARNING: Don't commit real credentials!
# Instead, use environment variables:
# import os
# email = os.getenv('ALERT_EMAIL')
# password = os.getenv('ALERT_PASSWORD')
#
email_handler = SMTPHandler(
    mailhost=('smtp.gmail.com', 587),          # Gmail SMTP server
    fromaddr='your_email@gmail.com',            # Sender address
    toaddrs=['ops@company.com'],                # Recipients list
    subject='[ALERT] Application Error',        # Email subject
    credentials=('your_email@gmail.com', 'app_specific_password'),  # Login
    secure=()                                   # Use TLS (tuple triggers STARTTLS)
)
email_handler.setLevel(logging.ERROR)           # Only ERROR and CRITICAL
email_handler.setFormatter(formatter)

# ============================================================================
# Attach all handlers to the logger
# ============================================================================
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.addHandler(email_handler)

# ============================================================================
# Test logging at different levels
# ============================================================================

def main():
    """Demonstrate logging output routing based on levels."""
    
    print("\n" + "="*60)
    print("Testing Logging with Multiple Handlers")
    print("="*60 + "\n")
    
    # DEBUG: File only
    # Destination: app2.log
    logger.debug("This is a debug message.")
    
    # INFO: File + Console
    # Destination: app2.log, stdout
    logger.info("This is an info message.")
    
    # WARNING: File + Console
    # Destination: app2.log, stdout
    logger.warning("This is a warning message.")
    
    # ERROR: File + Console + Email
    # Destination: app2.log, stdout, ops@company.com
    logger.error("This is an error message.")
    
    # CRITICAL: File + Console + Email
    # Destination: app2.log, stdout, ops@company.com
    logger.critical("This is a critical message.")
    
    print("\n" + "="*60)
    print("Logging Summary")
    print("="*60)
    print("DEBUG   → File only")
    print("INFO    → File + Console")
    print("WARNING → File + Console")
    print("ERROR   → File + Console + Email")
    print("CRITICAL→ File + Console + Email")
    print("\n")

# ============================================================================
# Alternative Setup: Rotating File Handler (recommended for production)
# ============================================================================
def setup_with_rotation():
    """Better setup that doesn't overflow disk with large log files."""
    from logging.handlers import RotatingFileHandler
    
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Rotating file handler: max 10MB per file, keep 5 backups
    # When app2.log reaches 10MB, it rotates to app2.log.1, .2, etc.
    file_handler = RotatingFileHandler(
        filename='app2.log',
        maxBytes=10*1024*1024,      # 10 MB
        backupCount=5               # Keep 5 old files
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    return logger

# ============================================================================
# Advanced Setup: Environment-based configuration
# ============================================================================
def setup_with_environment():
    """Configure logging based on environment (dev vs production)."""
    import os
    
    logger = logging.getLogger("my_logger")
    logger.setLevel(logging.DEBUG)
    
    env = os.getenv("ENV", "development")
    
    if env == "production":
        # Production: JSON format for log aggregation
        # from pythonjsonlogger import jsonlogger
        # formatter = jsonlogger.JsonFormatter()
        
        # File handler for persistence
        handler = logging.FileHandler('/var/log/app.log')
        handler.setLevel(logging.WARNING)  # Less verbose in production
        # handler.setFormatter(formatter)
        
        # Email handler for critical issues
        email_handler = SMTPHandler(
            mailhost=('smtp.gmail.com', 587),
            fromaddr=os.getenv('ALERT_EMAIL'),
            toaddrs=[os.getenv('OPS_EMAIL')],
            subject='[PRODUCTION] Critical Alert',
            credentials=(
                os.getenv('ALERT_EMAIL'),
                os.getenv('ALERT_PASSWORD')
            ),
            secure=()
        )
        email_handler.setLevel(logging.CRITICAL)
        logger.addHandler(handler)
        logger.addHandler(email_handler)
    
    else:
        # Development: Verbose console output
        formatter = logging.Formatter(
            '[%(levelname)s] %(name)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
    
    return logger

# ============================================================================
# Example: Using context with extra fields
# ============================================================================
def process_request(request_id, user_id, action):
    """Example showing structured logging with context."""
    
    logger.info(
        "Processing request",
        extra={
            'request_id': request_id,
            'user_id': user_id,
            'action': action
        }
    )
    
    try:
        # Simulate processing
        if action == "delete":
            logger.warning(
                "Destructive action requested",
                extra={
                    'request_id': request_id,
                    'action': action,
                    'severity': 'high'
                }
            )
    except Exception as e:
        logger.exception(
            "Request processing failed",
            extra={
                'request_id': request_id,
                'user_id': user_id,
                'error': str(e)
            }
        )
        raise

# ============================================================================
# Entry point
# ============================================================================
if __name__ == "__main__":
    main()
    
    # Uncomment to test other setups:
    # logger = setup_with_rotation()
    # logger.info("Using rotating file handler")
    
    # logger = setup_with_environment()
    # logger.info("Using environment-based configuration")
    
    # Test structured logging
    print("\n--- Testing with context ---\n")
    try:
        process_request("req-12345", 789, "delete")
    except:
        pass

"""
LOG ROUTING SUMMARY:

When you call logger.debug():
  1. Logger receives the LogRecord
  2. Checks against DEBUG level (passes)
  3. Sends to all attached handlers:
     - FileHandler @ DEBUG → Records to app2.log
     - StreamHandler @ INFO → Filters out (doesn't pass)
     - SMTPHandler @ ERROR → Filters out (doesn't pass)

When you call logger.error():
  1. Logger receives the LogRecord
  2. Checks against DEBUG level (passes)
  3. Sends to all attached handlers:
     - FileHandler @ DEBUG → Records to app2.log ✓
     - StreamHandler @ INFO → Passes, prints to console ✓
     - SMTPHandler @ ERROR → Passes, sends email ✓

PRODUCTION BEST PRACTICES:
1. ✓ Use RotatingFileHandler to prevent disk overflow
2. ✓ Use environment variables for credentials (never hardcode!)
3. ✓ Use JSON formatter for log aggregation platforms (ELK, Splunk)
4. ✓ Set different levels per handler for appropriate routing
5. ✓ Don't log sensitive data (passwords, tokens, credit cards)
6. ✓ Include request/trace IDs for debugging
7. ✓ Use appropriate log levels (don't spam with DEBUG in prod)
8. ✓ Consider async handlers for email (don't block on network)

COMPARISON WITH OTHER APPROACHES:
- Standard Logging: ✓ Good for simple apps, what this example shows
- JSON Logger: Better for log aggregation, add json formatter
- structlog: Better for microservices, easier context binding
"""
