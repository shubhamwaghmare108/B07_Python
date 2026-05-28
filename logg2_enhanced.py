"""
Enhanced logg2.py - structlog (Structured Logging) Example
===========================================================

structlog is a modern approach to logging that emphasizes:
- Structured data (context as key-value pairs, not strings)
- Context binding (request-level state that persists)
- Machine-readable output (JSON for log aggregation)
- Developer-friendly API

Installation:
    pip install structlog

Key Concepts:
- Processors: transform log records before output
- Context binding: bind() makes context persist
- Renderers: JSON (production) vs dev (development)
"""

import logging
import structlog
import sys

# ============================================================================
# BASIC SETUP - Your logg2.py example
# ============================================================================
def setup_basic():
    """Minimal structlog setup."""
    
    # Configure standard logging first (structlog uses it as fallback)
    logging.basicConfig(
        format="%(message)s",
        level=logging.INFO,
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),       # Add timestamp
            structlog.processors.add_log_level,                # Add level
            structlog.processors.JSONRenderer()                # JSON output
        ]
    )
    
    log = structlog.get_logger()
    log.info("server_started", port=5000)

# ============================================================================
# DEVELOPMENT SETUP - Pretty console output
# ============================================================================
def setup_development():
    """Configure for development with pretty console output."""
    
    logging.basicConfig(
        format="%(message)s",
        level=logging.DEBUG,
    )
    
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
    
    log = structlog.get_logger()
    return log

# ============================================================================
# PRODUCTION SETUP - JSON for log aggregation
# ============================================================================
def setup_production():
    """Configure for production with JSON output."""
    
    logging.basicConfig(
        format="%(message)s",
        level=logging.WARNING,  # Less verbose in production
    )
    
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer()  # Machine-readable
        ],
        context_class=dict,
        # Write to stdout (Docker/Kubernetes will capture it)
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )
    
    log = structlog.get_logger()
    return log

# ============================================================================
# KEY FEATURE: Context Binding
# ============================================================================
def demo_context_binding():
    """
    Context binding is structlog's killer feature.
    
    Bind context once, and all subsequent logs include it automatically.
    Perfect for request tracking in web apps.
    """
    
    setup_development()
    log = structlog.get_logger()
    
    print("\n" + "="*60)
    print("CONTEXT BINDING DEMO")
    print("="*60 + "\n")
    
    # Original logger has no context
    log.info("app_started")
    # Output: {'timestamp': '...', 'level': 'info', 'event': 'app_started'}
    
    # Bind context (request-specific info)
    request_logger = log.bind(
        request_id="req-12345",
        user_id=789,
        session_id="sess-abc"
    )
    
    # All logs from request_logger automatically include bound context
    request_logger.info("user_action", action="login")
    # Output: {'timestamp': '...', 'level': 'info', 'event': 'user_action', 
    #          'action': 'login', 'request_id': 'req-12345', 'user_id': 789, ...}
    
    request_logger.info("database_query", table="users", rows=10)
    # Output: {..., 'event': 'database_query', 'table': 'users', 'rows': 10,
    #          'request_id': 'req-12345', 'user_id': 789, ...}
    
    # Original logger still has no context
    log.info("other_event", data="xyz")
    # Output: {..., 'event': 'other_event', 'data': 'xyz'}
    # Notice: no request_id, user_id
    
    # Add more context to existing binding
    request_logger = request_logger.bind(endpoint="/api/users")
    request_logger.info("endpoint_accessed")
    # Output: {..., 'event': 'endpoint_accessed', 'endpoint': '/api/users',
    #          'request_id': 'req-12345', ...}

# ============================================================================
# EXCEPTION HANDLING
# ============================================================================
def demo_exception_handling():
    """Show how to log exceptions with structlog."""
    
    setup_development()
    log = structlog.get_logger()
    
    print("\n" + "="*60)
    print("EXCEPTION HANDLING DEMO")
    print("="*60 + "\n")
    
    try:
        # Simulate an error
        result = 10 / 0
    except ZeroDivisionError:
        # log.exception() automatically captures the traceback
        log.exception(
            "division_failed",
            numerator=10,
            denominator=0
        )
        # Output includes full traceback in 'exc_info'

# ============================================================================
# WEB FRAMEWORK INTEGRATION
# ============================================================================
def demo_web_integration():
    """Example of structlog in a web framework."""
    
    import uuid
    from datetime import datetime
    
    setup_production()
    log = structlog.get_logger()
    
    print("\n" + "="*60)
    print("WEB REQUEST TRACKING DEMO")
    print("="*60 + "\n")
    
    def handle_request(method, path, user_id):
        """Simulate a web request handler."""
        
        # Generate unique request ID
        request_id = str(uuid.uuid4())
        
        # Bind request context
        request_log = log.bind(
            request_id=request_id,
            method=method,
            path=path,
            user_id=user_id,
            timestamp_start=datetime.now().isoformat()
        )
        
        request_log.info("request_received")
        
        try:
            # Simulate request processing
            if path == "/users":
                request_log.info("fetching_users", limit=10)
                # ... database call ...
                request_log.info("users_fetched", count=5)
            
            elif path == "/delete":
                request_log.warning("destructive_operation", operation="delete")
                # ... process deletion ...
                request_log.info("operation_completed")
            
            request_log.info("request_completed", status=200)
            
        except Exception as e:
            request_log.exception("request_failed")
            # Output includes exception details + all bound context
    
    # Simulate multiple requests
    handle_request("GET", "/users", user_id=123)
    handle_request("DELETE", "/delete", user_id=456)

# ============================================================================
# PROCESSORS: Customizing Output
# ============================================================================
def demo_custom_processors():
    """Show how processors transform log records."""
    
    print("\n" + "="*60)
    print("CUSTOM PROCESSORS DEMO")
    print("="*60 + "\n")
    
    def sensitive_field_filter(logger, name, event_dict):
        """Remove sensitive fields before logging."""
        sensitive = {'password', 'token', 'api_key', 'secret'}
        for field in sensitive:
            if field in event_dict:
                event_dict[field] = "***REDACTED***"
        return event_dict
    
    logging.basicConfig(format="%(message)s", level=logging.INFO)
    
    structlog.configure(
        processors=[
            # Custom processor: remove sensitive data
            sensitive_field_filter,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
    )
    
    log = structlog.get_logger()
    
    # Without filter: password would be logged (BAD!)
    # With filter: password is redacted (GOOD!)
    log.info("user_login", username="alice", password="secret123")
    # Output: {..., 'username': 'alice', 'password': '***REDACTED***'}

# ============================================================================
# ADVANCED: Async Logging for Performance
# ============================================================================
def demo_async_logging():
    """
    For high-throughput applications, consider async logging
    to avoid blocking on I/O.
    """
    
    from pythonjsonlogger import jsonlogger
    from logging.handlers import QueueHandler, QueueListener
    from queue import Queue
    import threading
    
    print("\n" + "="*60)
    print("ASYNC LOGGING DEMO (Concept)")
    print("="*60 + "\n")
    
    # Create a queue for log records
    log_queue = Queue()
    
    # Handler that writes to actual file (runs in separate thread)
    actual_handler = logging.FileHandler('async_app.log')
    actual_handler.setFormatter(logging.Formatter('%(message)s'))
    
    # Start listener (processes queue in background)
    listener = QueueListener(log_queue, actual_handler)
    # listener.start()  # Uncomment to actually use
    
    # Queue handler (puts records in queue, returns immediately)
    queue_handler = QueueHandler(log_queue)
    
    logging.root.addHandler(queue_handler)
    logging.root.setLevel(logging.INFO)
    
    # Now logging calls return immediately
    # Actual I/O happens in background thread
    logger = logging.getLogger(__name__)
    logger.info("This returns immediately")
    
    # Note: listener.stop() needed before exit
    print("Async logging allows app to continue without I/O wait")

# ============================================================================
# BEST PRACTICES EXAMPLES
# ============================================================================
def demo_best_practices():
    """Show logging best practices with structlog."""
    
    setup_production()
    log = structlog.get_logger()
    
    print("\n" + "="*60)
    print("BEST PRACTICES")
    print("="*60 + "\n")
    
    # ✓ Good: Structured context with event name
    log.info("payment_processed", 
        transaction_id="txn-123",
        amount=99.99,
        currency="USD"
    )
    
    # ✓ Good: Bound context for related operations
    txn_log = log.bind(transaction_id="txn-123")
    txn_log.info("payment_initiated")
    txn_log.info("payment_authorized")
    txn_log.info("payment_settled")
    
    # ✓ Good: Use appropriate levels
    log.debug("Detailed info for developers")
    log.info("Important application events")
    log.warning("Something unexpected but recoverable")
    log.error("An operation failed")
    log.critical("System may not continue")
    
    # ✗ Bad: String formatting (don't do this)
    # log.info(f"Payment {amount} processed")
    
    # ✓ Good: Key-value pairs
    log.info("payment_received", amount=99.99)

# ============================================================================
# ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    # Run all demos
    demo_context_binding()
    demo_exception_handling()
    demo_web_integration()
    demo_custom_processors()
    demo_best_practices()
    
    print("\n" + "="*60)
    print("structlog Demo Complete")
    print("="*60 + "\n")

"""
KEY TAKEAWAYS:

1. CONTEXT BINDING is the killer feature
   - Bind once per request, included in all logs
   - Perfect for request tracing in microservices
   - Each service binds trace_id and passes it along

2. PRODUCTION READINESS
   - JSON output for log aggregation (ELK, Splunk, DataDog)
   - Write to stdout (Kubernetes/Docker captures it)
   - Use processors to redact sensitive data

3. DEVELOPER EXPERIENCE
   - Pretty console output in development (ConsoleRenderer)
   - JSON in production (JSONRenderer)
   - Same code works in both environments

4. COMPARISON WITH OTHER APPROACHES:
   
   Standard Logging:
   - Pros: Built-in, simple
   - Cons: No context binding, requires manual extra dict
   
   python-json-logger:
   - Pros: Drop-in addition to logging
   - Cons: Still uses standard logging API
   
   structlog:
   - Pros: Modern API, context binding, flexible processors
   - Cons: Requires learning new patterns

5. WHEN TO USE STRUCTLOG:
   ✓ Microservices with request tracking
   ✓ Large applications with complex logging
   ✓ Need to reduce logging boilerplate
   ✓ Building SaaS platforms
   
   When NOT to use:
   ✗ Simple scripts (use standard logging)
   ✗ Legacy code (too much refactoring)
   ✗ Team unfamiliar with structured logging

TYPICAL MIGRATION PATH:
1. Start: Standard logging (logging module)
2. Growth: Add python-json-logger
3. Scale: Migrate to structlog

INTEGRATION WITH LOG AGGREGATION:
App (structlog JSON) → stdout → Docker logs → Fluentd → Elasticsearch → Kibana
"""
