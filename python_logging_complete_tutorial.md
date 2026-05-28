# Complete Python Logging Tutorial
## Standard Logging, python-json-logger, and structlog

---

## Table of Contents
1. [Introduction](#introduction)
2. [Standard Logging Module](#standard-logging-module)
3. [python-json-logger](#python-json-logger)
4. [structlog](#structlog)
5. [Comparison and Selection Guide](#comparison-and-selection-guide)
6. [Best Practices](#best-practices)
7. [Real-World Examples](#real-world-examples)

---

## Introduction

Logging is crucial for:
- **Debugging**: Understanding what happened in production
- **Monitoring**: Tracking application health and performance
- **Auditing**: Recording user actions and system events
- **Alerting**: Detecting and responding to issues

### Log Levels (Severity)

| Level | Value | Use Case |
|-------|-------|----------|
| **DEBUG** | 10 | Detailed information for developers. Variables, function calls, intermediate steps. |
| **INFO** | 20 | General application flow. Server startup, user actions, completed operations. |
| **WARNING** | 30 | Something unexpected but recoverable. Deprecated usage, config issues. |
| **ERROR** | 40 | Something failed. Database errors, API timeouts, unrecovered exceptions. |
| **CRITICAL** | 50 | System may not continue. Shutdown imminent, data loss risk. |

---

## Standard Logging Module

Python's built-in `logging` module is the foundation for all logging.

### 1. Minimal Setup

```python
import logging

# Configure with basicConfig (one-liner)
logging.basicConfig(level=logging.DEBUG)

# Create logger
logger = logging.getLogger(__name__)

# Use it
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

**Output:**
```
DEBUG:__main__:Debug message
INFO:__main__:Info message
WARNING:__main__:Warning message
ERROR:__main__:Error message
CRITICAL:__main__:Critical message
```

### 2. Detailed Setup (Your logg.py Example)

```python
import logging

# Create logger
logger = logging.getLogger("my_logger")

# Configure with detailed format
logging.basicConfig(
    level=logging.DEBUG,
    filename='app1.log',
    filemode='a',  # append mode
    format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s '
            'module:(%(module)s) - function %(funcName)s:LineNo.%(lineno)d - %(message)s'
)

def division(a, b):
    logger.debug(f"Dividing {a} by {b}")
    c = a / b
    return c

# Test
try:
    division(10, 0)
except ZeroDivisionError as e:
    logger.debug(f"Error occurred while dividing: {e}")
    logger.exception(f"Error occurred: {e}")  # Includes traceback
    
logger.info("Division completed successfully.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")
```

**Output (app1.log):**
```
2024-12-15 10:30:45,123 - my_logger - DEBUG - logg.py module:(logg) - function division:LineNo.6 - Dividing 10 by 0
2024-12-15 10:30:45,125 - my_logger - DEBUG - logg.py module:(logg) - function <module>:LineNo.14 - Error occurred while dividing: division by zero
2024-12-15 10:30:45,126 - my_logger - ERROR - logg.py module:(logg) - function <module>:LineNo.15 - Error occurred: division by zero
Traceback (most recent call last):
  File "logg.py", line 10, in <module>
    division(10, 0)
  File "logg.py", line 6, in division
    c = a / b
ZeroDivisionError: division by zero
2024-12-15 10:30:45,127 - my_logger - INFO - logg.py module:(logg) - function <module>:LineNo.18 - Division completed successfully.
...
```

### 3. Format Attributes Reference

| Attribute | Description | Example |
|-----------|-------------|---------|
| `%(asctime)s` | Timestamp | `2024-12-15 10:30:45,123` |
| `%(name)s` | Logger name | `my_logger` |
| `%(levelname)s` | Log level | `ERROR` |
| `%(levelno)d` | Log level number | `40` |
| `%(filename)s` | Source filename | `app.py` |
| `%(funcName)s` | Function name | `division` |
| `%(lineno)d` | Line number | `25` |
| `%(module)s` | Module name | `app` |
| `%(pathname)s` | Full path | `/home/user/myapp/app.py` |
| `%(message)s` | Log message | `Error occurred` |
| `%(process)d` | Process ID | `12345` |
| `%(thread)d` | Thread ID | `139834829` |

### 4. Multiple Handlers (Your logg1.py Example)

```python
import logging
from logging.handlers import SMTPHandler

# Create logger
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# Define formatter (reuse for all handlers)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - '
    'function %(funcName)s:LineNo.%(lineno)d - %(message)s'
)

# Handler 1: File (captures DEBUG and above)
file_handler = logging.FileHandler('app2.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Handler 2: Console (INFO and above)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

# Handler 3: Email (ERRORS and above)
email_handler = SMTPHandler(
    mailhost=('smtp.gmail.com', 587),
    fromaddr='your_email@gmail.com',
    toaddrs=['admin@example.com'],
    subject='Application Error Notification',
    credentials=('your_email@gmail.com', 'app_specific_password'),
    secure=()  # Use TLS
)
email_handler.setLevel(logging.ERROR)
email_handler.setFormatter(formatter)

# Attach all handlers to logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
logger.addHandler(email_handler)

# Usage
logger.debug("This is a debug message.")      # File only
logger.info("This is an info message.")       # File + Console
logger.warning("This is a warning message.")  # File + Console
logger.error("This is an error message.")     # File + Console + Email
logger.critical("This is a critical message.") # File + Console + Email
```

**Log Flow:**
- DEBUG level → File only
- INFO level → File + Console
- WARNING level → File + Console
- ERROR level → File + Console + Email
- CRITICAL level → File + Console + Email

### 5. Exception Handling

```python
import logging

logger = logging.getLogger(__name__)

# Option 1: Use logger.exception() - automatically includes traceback
try:
    result = 10 / 0
except ZeroDivisionError:
    logger.exception("Division failed!")  # Includes full traceback

# Option 2: Use logger.error() with exc_info=True
try:
    result = 10 / 0
except ZeroDivisionError:
    logger.error("Division failed!", exc_info=True)  # Also includes traceback

# Option 3: Manually format exception
import traceback
try:
    result = 10 / 0
except ZeroDivisionError as e:
    logger.error(f"Division failed: {traceback.format_exc()}")
```

### 6. Logger Hierarchy

```python
import logging

# Loggers form a hierarchy with dots
logger_app = logging.getLogger("myapp")
logger_auth = logging.getLogger("myapp.auth")
logger_db = logging.getLogger("myapp.database")

# Configure parent logger (affects all children)
logging.getLogger("myapp").setLevel(logging.DEBUG)

# Override for specific module
logging.getLogger("myapp.database").setLevel(logging.INFO)  # Only INFO+

# Usage
logger_auth.debug("Auth debug")          # Will be shown (parent is DEBUG)
logger_db.debug("DB debug")              # Will NOT be shown (overridden to INFO)
logger_db.info("DB info")                # Will be shown
```

### 7. Common Handlers

```python
import logging
from logging.handlers import (
    RotatingFileHandler,      # Rotates by size
    TimedRotatingFileHandler, # Rotates by time
    SMTPHandler,              # Email
    SysLogHandler,            # System log
    MemoryHandler             # Buffer in memory
)

# Rotating by file size (keep 5 backup files of 1MB each)
handler = RotatingFileHandler(
    'app.log',
    maxBytes=1024*1024,  # 1MB
    backupCount=5
)

# Rotating by time (new log each day)
handler = TimedRotatingFileHandler(
    'app.log',
    when='midnight',
    interval=1,
    backupCount=7  # Keep 7 days
)

# Syslog (Linux/Mac)
handler = SysLogHandler(address='/dev/log')
```

---

## python-json-logger

Format logs as JSON for parsing by log aggregation platforms (ELK, Splunk, DataDog, New Relic).

### Installation

```bash
pip install python-json-logger
```

### 1. Basic Setup

```python
import logging
from pythonjsonlogger import jsonlogger

# Create logger
logger = logging.getLogger()

# Create handler and formatter
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Use it
logger.info("User login", extra={"user_id": 123, "ip": "192.168.1.1"})
```

**Output:**
```json
{"asctime": "2024-12-15 10:30:45,123", "name": "root", "levelname": "INFO", "message": "User login", "user_id": 123, "ip": "192.168.1.1"}
```

### 2. Custom Format

```python
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
handler = logging.FileHandler('app.log')

# Specify which fields to include
formatter = jsonlogger.JsonFormatter(
    '%(asctime)s %(name)s %(levelname)s %(message)s %(request_id)s %(user_id)s'
)
handler.setFormatter(formatter)
logger.addHandler(handler)

# Log with extra context
logger.info(
    "API request completed",
    extra={
        "request_id": "req-abc123",
        "user_id": 456,
        "duration_ms": 234
    }
)
```

**Output:**
```json
{"asctime": "2024-12-15 10:30:45,123", "name": "root", "levelname": "INFO", "message": "API request completed", "request_id": "req-abc123", "user_id": 456}
```

### 3. File Handler with JSON

```python
import logging
from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler

# JSON to file
file_handler = RotatingFileHandler('app.json.log', maxBytes=10485760, backupCount=10)
file_handler.setFormatter(jsonlogger.JsonFormatter())

# Text to console
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = logging.getLogger()
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)

logger.info("User action", extra={"action": "delete_account", "user_id": 789})
```

### 4. Querying JSON Logs with jq

```bash
# Print pretty JSON
jq '.' app.json.log

# Find all ERROR logs
jq 'select(.levelname == "ERROR")' app.json.log

# Find logs for specific user
jq 'select(.user_id == 123)' app.json.log

# Count logs by level
jq -s 'group_by(.levelname) | map({level: .[0].levelname, count: length})' app.json.log

# Filter by timestamp range
jq 'select(.asctime > "2024-12-15T10:00" and .asctime < "2024-12-15T11:00")' app.json.log
```

### 5. Integration with Log Aggregation

```python
# For ELK Stack (Elasticsearch, Logstash, Kibana)
import json
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
handler = logging.FileHandler('app.log')
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Logstash reads JSON from this file and ships to Elasticsearch
# Then Kibana visualizes it
logger.info("Transaction completed", extra={
    "transaction_id": "txn-12345",
    "amount": 99.99,
    "currency": "USD",
    "customer_id": 456
})
```

---

## structlog

Modern structured logging with context binding, perfect for microservices and complex applications.

### Installation

```bash
pip install structlog
```

### 1. Basic Setup (Your logg2.py Example)

```python
import logging
import structlog

# Configure standard logging
logging.basicConfig(
    format="%(message)s",
    level=logging.INFO,
)

# Configure structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),    # Add ISO timestamp
        structlog.processors.add_log_level,              # Add log level
        structlog.processors.JSONRenderer()              # Output as JSON
    ]
)

log = structlog.get_logger()

# Use it
log.info("server_started", port=5000, host="0.0.0.0")
```

**Output:**
```json
{"timestamp": "2024-12-15T10:30:45.123Z", "level": "info", "event": "server_started", "port": 5000, "host": "0.0.0.0"}
```

### 2. Context Binding (Key Feature)

Context binds variables that persist across all logs:

```python
import structlog

log = structlog.get_logger()

# Bind context (persists for all subsequent logs from this logger instance)
request_logger = log.bind(request_id="req-12345", user_id=789)

# These logs automatically include request_id and user_id
request_logger.info("user_action", action="login")
# Output: {"timestamp": "...", "level": "info", "event": "user_action", "action": "login", "request_id": "req-12345", "user_id": 789}

request_logger.info("database_query", table="users", rows=10)
# Output: {"timestamp": "...", "level": "info", "event": "database_query", "table": "users", "rows": 10, "request_id": "req-12345", "user_id": 789}

# Original logger unaffected
log.info("other_event", data="xyz")
# Output: {"timestamp": "...", "level": "info", "event": "other_event", "data": "xyz"}
```

### 3. Development vs Production Configuration

```python
import structlog
import sys

# Development: Pretty console output
def configure_dev():
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.dev.ConsoleRenderer()  # Pretty colors and formatting
        ],
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

# Production: JSON output to stdout (for container logs)
def configure_prod():
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer()  # Machine-parseable
        ],
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )

import os
if os.getenv("ENV") == "production":
    configure_prod()
else:
    configure_dev()

log = structlog.get_logger()
log.info("app_started", version="1.0.0")
```

### 4. Exception Handling

```python
import structlog

log = structlog.get_logger()

try:
    result = 10 / 0
except ZeroDivisionError:
    # Automatically includes full traceback
    log.exception("division_failed", operands=[10, 0])
    # Output includes "exc_info" with the full traceback
```

### 5. Processors: Customizing Output

Processors transform log records before output:

```python
import structlog

structlog.configure(
    processors=[
        # Add timestamp in ISO format
        structlog.processors.TimeStamper(fmt="iso"),
        
        # Add log level
        structlog.processors.add_log_level,
        
        # Render stack traces for exceptions
        structlog.processors.StackInfoRenderer(),
        
        # Format exception info
        structlog.processors.format_exc_info,
        
        # For development: pretty console output
        # structlog.dev.ConsoleRenderer()
        
        # For production: JSON output
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
    cache_logger_on_first_use=True,
)

log = structlog.get_logger()
log.info("processing_started", items=100)
```

### 6. Request Tracking in Web Apps

```python
import structlog
from uuid import uuid4

def middleware(app):
    """ASGI/WSGI middleware to bind request context"""
    async def asgi_middleware(scope, receive, send):
        request_id = str(uuid4())
        
        # Bind request context
        request_logger = structlog.get_logger().bind(
            request_id=request_id,
            method=scope["method"],
            path=scope["path"]
        )
        
        # Store in scope for handlers to access
        scope["logger"] = request_logger
        request_logger.info("request_received")
        
        await app(scope, receive, send)
        
        request_logger.info("request_completed")
    
    return asgi_middleware

# Usage in handler
def my_handler(request):
    log = request.scope["logger"]  # Has request_id bound
    log.info("processing_payment", amount=99.99)  # request_id automatically included
```

### 7. Filtering and Advanced Processing

```python
import structlog

def only_errors(logger, name, event_dict):
    """Only pass ERROR level and above"""
    if event_dict.get("level") not in ("error", "critical"):
        raise structlog.DropEvent()
    return event_dict

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        # only_errors,  # Uncomment to filter
        structlog.processors.JSONRenderer()
    ]
)
```

---

## Comparison and Selection Guide

### Feature Comparison

| Feature | Standard Logging | python-json-logger | structlog |
|---------|------------------|-------------------|-----------|
| **Built-in** | ✓ Yes | ✗ Requires pip | ✗ Requires pip |
| **Setup Complexity** | Simple | Simple | Medium |
| **Output Format** | Text (customizable) | JSON | JSON or text (customizable) |
| **Context Binding** | Extra dict per call | Extra dict per call | ✓ Persistent binding |
| **Log Aggregation Ready** | Works (parse text) | ✓ Perfect | ✓ Perfect |
| **Performance** | ✓ Very fast | Fast | Fast (async capable) |
| **Learning Curve** | Easy | Easy | Moderate |
| **Third-party Integration** | Limited | Good (ELK, Splunk) | Excellent (many platforms) |

### When to Use What

**Standard Logging:**
- ✓ Scripts and small projects
- ✓ Internal tools that don't need parsing
- ✓ When you want minimal dependencies
- ✓ Prototyping and quick testing

**python-json-logger:**
- ✓ Existing standard logging setup
- ✓ Apps using ELK Stack, Splunk, or DataDog
- ✓ Minimal migration effort needed
- ✓ Need JSON for log aggregation

**structlog:**
- ✓ Microservices architecture
- ✓ Request tracing across services
- ✓ Large, complex applications
- ✓ Rich context needed per request
- ✓ Development and production same codebase
- ✓ Team using modern Python practices

### Decision Flow

```
START: Choose a logging approach
  ↓
Do you need log aggregation?
  → NO → Standard logging (basic setup)
  → YES ↓
    Is context binding important?
      → NO → python-json-logger (add to existing setup)
      → YES → structlog (modern approach)
```

---

## Best Practices

### 1. Use Appropriate Log Levels

```python
import logging

logger = logging.getLogger(__name__)

# ✓ Good
logger.debug("Processing item", item_id=123)           # Dev details
logger.info("User login successful", user_id=456)      # App flow
logger.warning("Cache miss, using fallback", key="users")  # Unexpected
logger.error("Database connection failed")              # Operation failed
logger.critical("Out of memory, shutting down")         # Emergency

# ✗ Avoid
logger.info("x = 5")                  # Too granular
logger.error("Almost done")           # Not an error
logger.critical("Processing item")    # Normal, not critical
```

### 2. Include Structured Context

```python
# ✗ Bad: Information scattered in message string
logger.info(f"User {user_id} from {country} logged in")

# ✓ Good: Structured context
logger.info("user_login", extra={
    "user_id": user_id,
    "country": country,
    "ip_address": ip_address,
    "session_id": session_id
})

# ✓ With structlog
log = structlog.get_logger()
log = log.bind(user_id=user_id, session_id=session_id)
log.info("user_login", country=country, ip_address=ip_address)
```

### 3. Never Log Sensitive Data

```python
import logging
import hashlib

logger = logging.getLogger(__name__)

# ✗ Dangerous
password = "my_secret_password"
logger.info(f"Login: {username}:{password}")

# ✓ Safe: Don't log sensitive info at all
logger.info("login_attempted", username=username, success=True)

# ✓ Safe: Log hash instead of actual value
password_hash = hashlib.sha256(password.encode()).hexdigest()[:8]
logger.debug("password_validation", hash=password_hash)

# ✓ Safe: Mask sensitive data
def mask_credit_card(cc):
    return f"****-****-****-{cc[-4:]}"

logger.info("payment_processed", card=mask_credit_card(card_number))
```

### 4. Use Consistent Event Names

Pick a naming convention and stick to it:

```python
# Option A: snake_case
log.info("user_signup", email="user@example.com")
log.info("payment_processed", amount=99.99)
log.info("email_sent", recipient="admin@example.com")

# Option B: domain.event
log.info("auth.user_signup", email="user@example.com")
log.info("payment.processed", amount=99.99)
log.info("email.sent", recipient="admin@example.com")

# Be consistent within your codebase
```

### 5. Handle Exceptions Properly

```python
import logging
import traceback

logger = logging.getLogger(__name__)

# ✗ Silent failure (don't do this!)
try:
    process_payment(user_id=123)
except PaymentError:
    pass  # Invisible error!

# ✓ Log with context
try:
    process_payment(user_id=123)
except PaymentError as e:
    logger.exception("payment_failed", user_id=123)  # Includes traceback
    # Handle or re-raise
    raise

# ✓ Log specific error details
try:
    process_payment(user_id=123, amount=99.99)
except PaymentError as e:
    logger.error(
        "payment_failed",
        extra={
            "user_id": 123,
            "amount": 99.99,
            "error_code": e.code,
            "error_message": str(e)
        }
    )
```

### 6. Use Logger Hierarchy

```python
import logging

# Create loggers in hierarchy
logger = logging.getLogger(__name__)  # "myapp.auth"
logger_db = logging.getLogger("myapp.database")
logger_api = logging.getLogger("myapp.api")

# Configure at parent level
logging.getLogger("myapp").setLevel(logging.DEBUG)

# Override for specific module
logging.getLogger("myapp.database").setLevel(logging.WARNING)

# Usage
logger_db.debug("Query executed")  # NOT shown (level is WARNING)
logger_db.warning("Query slow")    # Shown
logger.info("Auth check passed")   # Shown (parent DEBUG applies)
```

### 7. Separate Concerns with Multiple Handlers

```python
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

logger = logging.getLogger("myapp")
logger.setLevel(logging.DEBUG)

# All logs to file
file_handler = RotatingFileHandler('app.log', maxBytes=10485760, backupCount=5)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Console: only INFO and above
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
logger.addHandler(console_handler)

# Email: only CRITICAL
email_handler = SMTPHandler(
    mailhost='smtp.gmail.com',
    fromaddr='app@example.com',
    toaddrs=['ops@example.com'],
    subject='CRITICAL: Application Error'
)
email_handler.setLevel(logging.CRITICAL)
logger.addHandler(email_handler)

# Usage
logger.debug("Debug info")      # File only
logger.info("User login")       # File + Console
logger.error("DB error")        # File + Console
logger.critical("System down")  # File + Console + Email
```

### 8. Configure for Environment

```python
import os
import logging

def configure_logging():
    if os.getenv("ENV") == "production":
        log_level = logging.WARNING
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        filename = '/var/log/myapp.log'
    else:
        log_level = logging.DEBUG
        log_format = '%(asctime)s [%(name)s] %(levelname)s (%(filename)s:%(lineno)d): %(message)s'
        filename = 'myapp.log'
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        filename=filename
    )

configure_logging()
```

### 9. Avoid Performance Issues

```python
import logging

logger = logging.getLogger(__name__)

# ✗ Bad: Expensive operation always runs
large_data = expensive_function()
logger.debug(f"Data: {large_data}")  # f-string evaluated even if DEBUG disabled!

# ✓ Good: Only evaluate if level enabled
if logger.isEnabledFor(logging.DEBUG):
    large_data = expensive_function()
    logger.debug(f"Data: {large_data}")

# ✓ Even better: Use lazy formatting
logger.debug("Data: %s", expensive_function)  # Function passed, not called
```

### 10. Centralized Log Aggregation

For production: Application → Logs → Log Shipper → Platform

```python
import structlog
import sys
import json

# Write JSON to stdout (container/Kubernetes captures this)
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
)

log = structlog.get_logger()
log.info("app_started", version="1.0.0")

# In Docker: stdout → Docker logs → Fluentd/Filebeat → Elasticsearch/Splunk
# Enable with docker logs <container>, or use logging driver
```

---

## Real-World Examples

### Example 1: Web API with Structured Logging

```python
import structlog
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

# Configure structlog
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory(),
)

app = FastAPI()
log = structlog.get_logger()

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    
    # Bind request context
    request_log = log.bind(
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        client_ip=request.client.host
    )
    
    request_log.info("request_started")
    
    try:
        response = await call_next(request)
        request_log.info("request_completed", status_code=response.status_code)
        return response
    except Exception as exc:
        request_log.exception("request_failed")
        return JSONResponse({"error": "Internal Server Error"}, status_code=500)

@app.post("/users")
async def create_user(email: str):
    request_log = log.bind(endpoint="/users")
    request_log.info("creating_user", email=email)
    
    # Create user...
    user_id = 123
    
    request_log.info("user_created", user_id=user_id)
    return {"user_id": user_id, "email": email}
```

### Example 2: Database Operations with Context

```python
import logging
from pythonjsonlogger import jsonlogger
import time

logger = logging.getLogger("database")
handler = logging.FileHandler('db.log')
handler.setFormatter(jsonlogger.JsonFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class Database:
    def __init__(self, connection_string):
        self.conn_string = connection_string
        self.logger = logger
    
    def execute_query(self, query, params=None):
        request_id = params.get('request_id') if params else None
        start = time.time()
        
        try:
            # Execute query
            result = self._execute(query, params)
            duration_ms = (time.time() - start) * 1000
            
            self.logger.info(
                "query_executed",
                extra={
                    "query": query[:100],  # Log first 100 chars
                    "request_id": request_id,
                    "duration_ms": duration_ms,
                    "rows_affected": len(result)
                }
            )
            return result
        
        except Exception as e:
            duration_ms = (time.time() - start) * 1000
            self.logger.exception(
                "query_failed",
                extra={
                    "query": query[:100],
                    "request_id": request_id,
                    "duration_ms": duration_ms,
                    "error": str(e)
                }
            )
            raise
    
    def _execute(self, query, params):
        # Actual execution
        return []
```

### Example 3: Multi-Service with Trace ID

```python
import structlog
import uuid
import requests

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ],
)

def call_service(service_url, data, trace_id=None):
    if not trace_id:
        trace_id = str(uuid.uuid4())
    
    log = structlog.get_logger().bind(trace_id=trace_id, service=service_url)
    log.info("calling_service", payload=data)
    
    try:
        response = requests.post(
            service_url,
            json=data,
            headers={"X-Trace-ID": trace_id}  # Pass trace ID to service
        )
        response.raise_for_status()
        log.info("service_success", status=response.status_code)
        return response.json()
    
    except requests.RequestException as e:
        log.exception("service_failed", error=str(e))
        raise

# Usage
trace_id = str(uuid.uuid4())
result = call_service("https://api.example.com/process", {"data": "xyz"}, trace_id)
```

---

## Summary

| Approach | Best For | Setup | Output |
|----------|----------|-------|--------|
| **Standard Logging** | Small projects, scripts | Simple (1 config) | Plain text |
| **python-json-logger** | Log aggregation (ELK, Splunk) | Simple (add to existing) | JSON |
| **structlog** | Microservices, complex apps | Medium (more config) | JSON + context |

**Start simple, evolve as needs grow:** Script → Standard Logging → python-json-logger → structlog

---

## Additional Resources

- [Python logging documentation](https://docs.python.org/3/library/logging.html)
- [python-json-logger GitHub](https://github.com/madzak/python-json-logger)
- [structlog documentation](https://www.structlog.org/)
- [ELK Stack setup](https://www.elastic.co/what-is/elk-stack)
- [Splunk for logging](https://www.splunk.com/)
