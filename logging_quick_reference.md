# Python Logging: Quick Reference Cheat Sheet

## One-Liner Setups

### Standard Logging (Minimal)
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.info("Hello world")
```

### Standard Logging (With File)
```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    filename='app.log',
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### JSON Logging
```python
import logging
from pythonjsonlogger import jsonlogger
handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter())
logging.root.addHandler(handler)
logger = logging.getLogger(__name__)
logger.info("Event", extra={"field": "value"})
```

### structlog
```python
import structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ]
)
log = structlog.get_logger()
log.info("event", key="value")
```

---

## Log Levels Quick Reference

| Level | Use When |
|-------|----------|
| `DEBUG` | Detailed info for developers (variable values, function calls) |
| `INFO` | Important application events (startup, user actions, operations) |
| `WARNING` | Something unexpected but not critical (deprecated usage, slow queries) |
| `ERROR` | Something failed (exception, failed operation) |
| `CRITICAL` | System may not continue (shutdown, data loss risk) |

```python
logger.debug("var x = %s", x)
logger.info("User %s logged in", username)
logger.warning("Connection timeout, retrying...")
logger.error("Database connection failed")
logger.critical("Out of memory")
```

---

## Common Handlers

```python
import logging
from logging.handlers import FileHandler, StreamHandler, RotatingFileHandler, SMTPHandler

# Console output
handler = StreamHandler()

# File output
handler = FileHandler('app.log')

# Rotating file (by size)
handler = RotatingFileHandler('app.log', maxBytes=10485760, backupCount=5)

# Rotating file (by time)
from logging.handlers import TimedRotatingFileHandler
handler = TimedRotatingFileHandler('app.log', when='midnight', backupCount=7)

# Email alerts
handler = SMTPHandler(
    mailhost='smtp.gmail.com',
    fromaddr='app@example.com',
    toaddrs=['admin@example.com'],
    subject='App Error',
    credentials=('email', 'password'),
    secure=()
)

# Add to logger
logger.addHandler(handler)
```

---

## Format Attributes

```python
# Common format string
'%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'

# All available attributes:
%(asctime)s      # Timestamp
%(name)s         # Logger name
%(levelname)s    # Level (DEBUG, INFO, etc)
%(levelno)d      # Level number (10, 20, 30, etc)
%(message)s      # Log message
%(filename)s     # Source filename
%(funcName)s     # Function name
%(lineno)d       # Line number
%(module)s       # Module name
%(pathname)s     # Full file path
%(process)d      # Process ID
%(thread)d       # Thread ID
```

---

## Exception Logging

```python
# Automatically includes traceback
try:
    1/0
except Exception:
    logger.exception("Division failed")

# Or explicitly
except Exception as e:
    logger.error("Division failed", exc_info=True)
```

---

## Context/Extra Fields

```python
# Standard logging
logger.info("User action", extra={
    "user_id": 123,
    "action": "login",
    "ip": "192.168.1.1"
})

# python-json-logger (same syntax)
logger.info("User action", extra={
    "user_id": 123,
    "action": "login",
    "ip": "192.168.1.1"
})

# structlog (context binding)
log = structlog.get_logger()
request_log = log.bind(user_id=123, request_id="req-123")
request_log.info("user_action", action="login")
```

---

## Logger Hierarchy

```python
# Create loggers in hierarchy
auth_logger = logging.getLogger("myapp.auth")
db_logger = logging.getLogger("myapp.database")
api_logger = logging.getLogger("myapp.api")

# Configure parent (affects all children)
logging.getLogger("myapp").setLevel(logging.DEBUG)

# Override specific child
logging.getLogger("myapp.database").setLevel(logging.WARNING)
```

---

## Multiple Handlers Example

```python
logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

# File: All levels
file_handler = FileHandler('app.log')
file_handler.setLevel(logging.DEBUG)

# Console: Info and above
console_handler = StreamHandler()
console_handler.setLevel(logging.INFO)

# Email: Critical only
email_handler = SMTPHandler(...)
email_handler.setLevel(logging.CRITICAL)

# Add all
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(email_handler)

# Result:
# DEBUG   → File only
# INFO    → File + Console
# WARNING → File + Console
# ERROR   → File + Console
# CRITICAL→ File + Console + Email
```

---

## Production Configuration

```python
import os
import logging

def setup_logging():
    env = os.getenv("ENV", "development")
    
    if env == "production":
        level = logging.WARNING
        format_str = '%(asctime)s - %(levelname)s - %(message)s'
        filename = '/var/log/app.log'
    else:
        level = logging.DEBUG
        format_str = '[%(levelname)s] %(name)s: %(message)s'
        filename = 'app.log'
    
    logging.basicConfig(
        level=level,
        format=format_str,
        filename=filename
    )

setup_logging()
```

---

## Environment-Based structlog

```python
import os
import structlog

env = os.getenv("ENV", "development")

if env == "production":
    # JSON for log aggregation
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer()
        ]
    )
else:
    # Pretty console for development
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.dev.ConsoleRenderer()
        ]
    )

log = structlog.get_logger()
```

---

## Common Mistakes to Avoid

```python
# ✗ Don't: Silent failures
try:
    dangerous_operation()
except Exception:
    pass  # Silent!

# ✓ Do: Log exceptions
except Exception:
    logger.exception("Operation failed")

# ✗ Don't: Sensitive data
logger.info(f"User {username}:{password} logged in")

# ✓ Do: Safe logging
logger.info("User login", extra={"username": username, "success": True})

# ✗ Don't: String formatting always
logger.debug(f"Expensive operation: {expensive_func()}")

# ✓ Do: Lazy evaluation
logger.debug("Expensive operation: %s", expensive_func)

# ✗ Don't: Generic messages
logger.warning("Something happened")

# ✓ Do: Specific context
logger.warning("Cache miss", extra={"key": "users", "ttl": 60})

# ✗ Don't: Inconsistent level usage
logger.error("Almost done")  # Not an error!

# ✓ Do: Appropriate levels
logger.info("Processing completed")  # INFO level

# ✗ Don't: Lose context in microservices
def service_call(data):
    logger.info(f"Processing {data}")

# ✓ Do: Pass trace ID
def service_call(data, trace_id):
    request_log = log.bind(trace_id=trace_id)
    request_log.info("processing", data=data)
```

---

## JSON Log Querying (jq)

```bash
# Pretty print
jq '.' app.log

# Find errors
jq 'select(.levelname == "ERROR")' app.log

# Find specific user
jq 'select(.user_id == 123)' app.log

# Get all unique events
jq '.event' app.log | sort | uniq

# Count by level
jq -s 'group_by(.levelname) | map({level: .[0].levelname, count: length})' app.log

# Filter by time range
jq 'select(.timestamp > "2024-12-15T10:00" and .timestamp < "2024-12-15T11:00")' app.log

# Extract specific fields
jq '{timestamp, event, user_id}' app.log
```

---

## Decision Tree

```
Start: "I need logging"
  ↓
Is it a simple script?
  YES → Use standard logging ✓
  NO ↓
    
Do you need to parse logs programmatically?
  NO → Use standard logging with file handler ✓
  YES ↓
    
Do you have a log aggregation platform (ELK, Splunk, DataDog)?
  NO → Use standard logging ✓
  YES ↓
    
Is it a microservices architecture?
  NO → Use python-json-logger ✓
  YES → Use structlog ✓
```

---

## Installation Commands

```bash
# Standard logging: included (no installation needed)

# JSON logger
pip install python-json-logger

# structlog
pip install structlog

# Both JSON and structlog
pip install python-json-logger structlog
```

---

## Testing Logging

```python
import logging
from unittest.mock import patch

def test_logging():
    with patch('logging.Logger.info') as mock_info:
        logger = logging.getLogger()
        logger.info("Test message", extra={"key": "value"})
        
        mock_info.assert_called_once_with("Test message", extra={"key": "value"})

# Or capture logs
import logging.handlers

def test_with_capture():
    logger = logging.getLogger("test")
    handler = logging.StreamHandler()
    logger.addHandler(handler)
    
    logger.info("Test message")
    # Assert handler received the message
```

---

## Performance Tips

```python
# ✗ Expensive: Evaluate every time
logger.debug(f"Data: {slow_function()}")

# ✓ Better: Check before evaluating
if logger.isEnabledFor(logging.DEBUG):
    logger.debug(f"Data: {slow_function()}")

# ✓ Best: Use lazy formatting
logger.debug("Data: %s", slow_function)  # Only called if DEBUG enabled

# Use async handlers for I/O
from logging.handlers import QueueHandler
handler = QueueHandler(queue)
logger.addHandler(handler)
```

---

## Quick Comparison

| Task | Standard | JSON Logger | structlog |
|------|----------|-------------|-----------|
| Simple logging | ✓ Easy | ✓ Easy | ✓ Easy |
| Multiple handlers | ✓ Easy | ✓ Easy | Medium |
| Context binding | Repetitive | Repetitive | ✓ Native |
| Log aggregation | Extra work | ✓ Ready | ✓ Ready |
| Microservices | Works | Works | ✓ Best |
| Learning curve | Minimal | Minimal | Medium |

---

## Resources

- [Python logging docs](https://docs.python.org/3/library/logging.html)
- [python-json-logger](https://github.com/madzak/python-json-logger)
- [structlog docs](https://www.structlog.org/)
- [Logging best practices](https://docs.python-guide.org/writing/logging/)

---

## Remember

1. **Log important events**, not every line of code
2. **Use appropriate levels** (don't abuse WARNING for info)
3. **Never log sensitive data** (passwords, tokens, PII)
4. **Include context** (user_id, request_id, etc)
5. **Consistent naming** (use same event names everywhere)
6. **Test logging** (ensure it works in production)
7. **Plan for scale** (use handlers/aggregation early)
8. **Start simple**, upgrade as needs grow
