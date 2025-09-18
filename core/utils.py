# core/utils.py
"""
Shared utility functions for logging and debugging.
"""
import logging

# Set up named loggers
logging.basicConfig(level=logging.INFO)

info_logger = logging.getLogger('info')
error_logger = logging.getLogger('error')

# Console handler (optional)
if not info_logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    info_logger.addHandler(handler)
    error_logger.addHandler(handler)

def log_info(message):
    """
    Log an info message.
    """
    info_logger.info(message)

def log_error(message):
    """
    Log an error message.
    """
    error_logger.error(message)