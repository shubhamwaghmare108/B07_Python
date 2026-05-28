# Python Logging: Complete Comparison Guide

## Quick Reference Table

| Feature | Standard Logging | python-json-logger | structlog |
|---------|------------------|-------------------|-----------|
| **Built-in?** | ✓ Yes | ✗ Requires pip | ✗ Requires pip |
| **Installation** | None | `pip install python-json-logger` | `pip install structlog` |
| **Setup Time** | 2 minutes | 2 minutes | 5 minutes |
| **Learning Curve** | Easy | Easy | Medium |
| **Output Format** | Text (customizable) | JSON | JSON or text |
| **Context Binding** | Extra dict per call | Extra dict per call | ✓ Persistent binding |
| **Log Aggregation Ready** | Partial (needs parsing) | ✓ Perfect | ✓ Perfect |
| **Performance** | ✓ Very fast | ✓ Fast | ✓ Fast |
| **Async Support** | ✓ QueueHandler | ✓ QueueHandler | ✓ Native |
| **Team Adoption** | ✓ Familiar | ✓ Easy (minimal change) | Moderate (new patterns) |
| **Code Example Size** | Small | Small | Medium |
| **Production Ready** | ✓ With handlers | ✓ Yes | ✓ Yes |
| **Microservices Ready** | Works | Works | ✓ Excellent |

---

## Detailed Comparison

### 1. Standard Logging (Python Built-in)

**Best For:**
- Small projects and scripts
- Internal tools
- Prototyping
- Teams unfamiliar with logging best practices

**Pros:**
- ✓ No external dependencies
- ✓ Familiar to most Python developers
- ✓ Very fast
- ✓ Flexible formatting
- ✓ Multiple handlers out of the box

**Cons:**
- ✗ Text output (hard to parse programmatically)
- ✗ Context must be added per-call (repetitive)
- ✗ No built-in context binding
- ✗ String formatting can be verbose

**Example:**
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename='app.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info("User logged in", extra={"user_id": 123, "ip": "192.168.1.1"})
```

**Output:**
```
2024-12-15 10:30:45,123 - __main__ - INFO - User logged in
```

**Good For:**
```python
# Simple scripts
def main():
    logger.info("Processing started")
    for item in items:
        logger.debug(f"Processing {item}")
    logger.info("Processing completed")
```

**Not Good For:**
```python
# Microservices (loses context between services)
# High-volume apps needing log aggregation
# Complex request tracking
```

---

### 2. python-json-logger

**Best For:**
- Apps using log aggregation platforms (ELK, Splunk, DataDog)
- Projects with existing logging setup
- Teams wanting JSON without major refactoring
- Machine-readable logs needed

**Pros:**
- ✓ Drop-in addition to existing logging
- ✓ JSON output for log aggregation
- ✓ Minimal code changes
- ✓ Works with all logging handlers
- ✓ Easy to query/filter logs

**Cons:**
- ✗ Still uses logging's verbose API
- ✗ Context still per-call (not bound)
- ✗ Extra dependency
- ✗ Slightly slower than standard logging

**Example:**
```python
import logging
from pythonjsonlogger import jsonlogger

handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.addHandler(handler)

logger.info("User logged in", extra={"user_id": 123, "ip": "192.168.1.1"})
```

**Output:**
```json
{"asctime": "2024-12-15 10:30:45,123", "name": "root", "levelname": "INFO", "message": "User logged in", "user_id": 123, "ip": "192.168.1.1"}
```

**Good For:**
```python
# Adding to existing logging setup
logger.info("payment_processed", extra={
    "transaction_id": "txn-123",
    "amount": 99.99,
    "currency": "USD"
})

# Querying with jq
# jq 'select(.levelname == "ERROR")' app.log
```

**Integration Example:**
```python
# ELK Stack Integration
# App writes JSON → Logstash reads → Elasticsearch stores → Kibana visualizes

import logging
from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('app.log', maxBytes=1024*1024*10, backupCount=10)
handler.setFormatter(jsonlogger.JsonFormatter())
logging.root.addHandler(handler)

# Logstash config:
# input {
#   file {
#     path => "/path/to/app.log"
#     codec => json
#   }
# }
```

---

### 3. structlog (Modern)

**Best For:**
- Microservices architecture
- Request tracing across services
- Large, complex applications
- When context binding is essential
- Development AND production same code

**Pros:**
- ✓ Native context binding (request-level persistence)
- ✓ Modern, clean API
- ✓ Flexible processors
- ✓ Perfect for microservices
- ✓ Development/production same code
- ✓ Async capable
- ✓ Excellent for distributed tracing

**Cons:**
- ✗ New API (learning curve)
- ✗ Extra dependency
- ✗ More complex configuration
- ✗ Overkill for simple projects

**Example:**
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

# Bind context (persists for all logs)
request_log = log.bind(request_id="req-123", user_id=456)

request_log.info("user_action", action="login")
request_log.info("database_query", table="users")  # request_id included automatically
```

**Output:**
```json
{"timestamp": "2024-12-15T10:30:45.123Z", "level": "info", "event": "user_action", "action": "login", "request_id": "req-123", "user_id": 456}
{"timestamp": "2024-12-15T10:30:45.124Z", "level": "info", "event": "database_query", "table": "users", "request_id": "req-123", "user_id": 456}
```

**Good For:**
```python
# Microservices: Request flows across multiple services
import uuid
import structlog

log = structlog.get_logger()

def handle_request(request_data):
    # Generate trace ID once
    trace_id = str(uuid.uuid4())
    request_log = log.bind(trace_id=trace_id, service="api-gateway")
    
    request_log.info("request_received", method="POST", path="/api/users")
    
    # Call another service with same trace_id
    user_service_log = structlog.get_logger().bind(
        trace_id=trace_id,  # SAME trace_id
        service="user-service"
    )
    user_service_log.info("fetching_user", user_id=123)
    
    # Now you can trace the entire request flow across services!
```

**Context Binding (Key Feature):**
```python
# Without binding (repetitive):
logger.info("event1", user_id=123, request_id="req-abc")
logger.info("event2", user_id=123, request_id="req-abc")
logger.info("event3", user_id=123, request_id="req-abc")

# With binding (clean):
request_log = logger.bind(user_id=123, request_id="req-abc")
request_log.info("event1")
request_log.info("event2")
request_log.info("event3")
```

---

## Decision Matrix: Which Should You Use?

### Scenario 1: New Small Project
```
↓ Is it a simple script?
YES → Standard Logging ✓
NO ↓

↓ Do you need log aggregation?
NO → Standard Logging ✓
YES ↓

↓ Is it microservices?
NO → python-json-logger ✓
YES → structlog ✓
```

### Scenario 2: Existing Large App
```
↓ Currently using logging module?
NO → Start with structlog
YES ↓

↓ Need log aggregation?
NO → Stay with standard logging
YES ↓

↓ Planning microservices?
NO → Add python-json-logger (minimal change)
YES → Migrate to structlog
```

### Scenario 3: Building SaaS Platform
```
→ Use structlog from day 1
  - Request tracing across services
  - Context binding for complex flows
  - Development and production same code
  - Ready for log aggregation
```

---

## Code Migration Path

### From Standard Logging to python-json-logger

**Before:**
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("User logged in", extra={"user_id": 123})
```

**After (minimal change):**
```python
import logging
from pythonjsonlogger import jsonlogger

handler = logging.StreamHandler()
handler.setFormatter(jsonlogger.JsonFormatter())
logging.root.addHandler(handler)

logger = logging.getLogger(__name__)
logger.info("User logged in", extra={"user_id": 123})  # Same call!
```

### From Standard Logging to structlog

**Before:**
```python
import logging

logger = logging.getLogger(__name__)

def process_request(request_id, user_id):
    logger.info("Processing", extra={
        "request_id": request_id,
        "user_id": user_id
    })
    logger.info("Saving", extra={
        "request_id": request_id,
        "user_id": user_id
    })
```

**After (cleaner):**
```python
import structlog

log = structlog.get_logger()

def process_request(request_id, user_id):
    request_log = log.bind(request_id=request_id, user_id=user_id)
    request_log.info("Processing")
    request_log.info("Saving")
```

---

## Production Setup Examples

### Example 1: Simple Production App
```python
# Use standard logging with multiple handlers
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("myapp")
logger.setLevel(logging.INFO)

# File handler
file_handler = RotatingFileHandler('app.log', maxBytes=10485760, backupCount=5)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)  # Less verbose

logger.addHandler(file_handler)
logger.addHandler(console_handler)
```

### Example 2: App with Log Aggregation
```python
# Use python-json-logger
import logging
from pythonjsonlogger import jsonlogger
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("myapp")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler('app.log', maxBytes=10485760, backupCount=5)
handler.setFormatter(jsonlogger.JsonFormatter())
logger.addHandler(handler)

# Logstash/Fluentd reads JSON and ships to ELK, Splunk, etc.
```

### Example 3: Microservices Platform
```python
# Use structlog with distributed tracing
import structlog
import sys
import uuid

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
)

# In FastAPI middleware:
@app.middleware("http")
async def add_trace_id(request, call_next):
    trace_id = request.headers.get("X-Trace-ID", str(uuid.uuid4()))
    request.state.log = structlog.get_logger().bind(trace_id=trace_id)
    response = await call_next(request)
    return response

# In handlers:
async def handler(request):
    request.state.log.info("handling_request")
```

---

## Performance Comparison

### Logging Overhead (approximate)

| Approach | Time per log | Notes |
|----------|-------------|-------|
| Standard logging (no file write) | 0.1ms | Console only |
| Standard logging (file write) | 1-5ms | Depends on disk |
| python-json-logger (JSON parsing) | 0.2ms | Slight overhead |
| structlog (simple processor) | 0.15ms | Very efficient |
| Any async handler | <0.01ms | Offloads to thread |

**Recommendation:** For most apps, performance is NOT the bottleneck. Choose based on features, not microseconds.

---

## Checklist: Choosing Your Logging Approach

### For Standard Logging
- [ ] Small project (< 5000 lines)
- [ ] Single service (not microservices)
- [ ] No log aggregation platform
- [ ] Team familiar with logging module
- [ ] Quick prototyping

### For python-json-logger
- [ ] Existing logging setup you want to keep
- [ ] Using ELK Stack, Splunk, DataDog, or similar
- [ ] Need machine-readable logs
- [ ] Minimal code changes desired
- [ ] Don't need context binding

### For structlog
- [ ] Microservices architecture
- [ ] Request tracing across services
- [ ] Complex application with many features
- [ ] Need context binding per request
- [ ] Development and production same code
- [ ] Team willing to learn new patterns
- [ ] Plan long-term growth

---

## Summary Table: When to Migrate

| Current State | Action |
|---------------|--------|
| Using print() statements | Migrate to standard logging immediately |
| Using standard logging | Keep if satisfied |
| Using standard logging + need log aggregation | Add python-json-logger (minimal change) |
| Building microservices | Use structlog from day 1 |
| Large app with complex logging | Migrate to structlog (gradual) |
| Team new to Python | Start with standard logging, evolve as needed |

---

## Additional Resources

### Official Documentation
- [Python logging](https://docs.python.org/3/library/logging.html)
- [python-json-logger](https://github.com/madzak/python-json-logger)
- [structlog](https://www.structlog.org/)

### Tutorials
- ELK Stack setup: https://www.elastic.co/what-is/elk-stack
- Splunk: https://www.splunk.com/
- DataDog: https://www.datadoghq.com/

### Best Practices
- [Logging Best Practices](https://www.pythonsharedlibrary.org/logging-best-practices/)
- [Structured Logging](https://www.kartar.net/2015/12/structured-logging/)

---

## Final Recommendation

**If in doubt: Start with standard logging.**

Upgrade to python-json-logger when you add log aggregation platform.
Migrate to structlog if you build microservices.

The Python logging ecosystem is designed for this evolution.
Each tool is appropriate for its scope.

Remember: Good logging practices matter more than the tool.
Always log:
- ✓ What happened
- ✓ When it happened
- ✓ Who/what it affected
- ✗ Never log sensitive data
