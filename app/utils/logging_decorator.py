import logging
import functools

logger = logging.getLogger("service_logger")


def service_log(func):
    """
    Decorator to log entry, exit, and exceptions for service methods.
    Logs method name, arguments, return value, and exceptions.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Entering {func.__qualname__} args={args} kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Exiting {func.__qualname__} result={result}")
            return result
        except Exception as e:
            logger.exception(f"Exception in {func.__qualname__}: {e}")
            raise
    return wrapper
