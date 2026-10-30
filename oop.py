import logging

root = logging.getLogger()
root.setLevel(logging.ERROR)

handler = logging.StreamHandler()
handler.setLevel(logging.WARNING)
root.addHandler(handler)

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

logger.propagate = False  # Prevent log messages from propagating to the root logger
logger.debug("A")
logger.info("B")
logger.warning("C")
logger.error("D")