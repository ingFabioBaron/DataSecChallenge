# common/logging_config.py

"""
Logging configuration utility for the entire project.

Provides a consistent logger with the following features:
- Default log level: INFO
- Respects the LOG_LEVEL environment variable if defined
- Avoids adding duplicate handlers for the same logger
"""

import logging
import os


def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger for a given module.

    Parameters:
    ----------
    name : str
        Name of the logger, usually __name__ of the module.

    Returns:
    -------
    logging.Logger
        Configured logger instance.
    """

    # ============================================================
    # Create or get existing logger
    # ============================================================
    logger = logging.getLogger(name)

    if not logger.handlers:
        # ========================================================
        # Determine log level from environment variable, default INFO
        # ========================================================
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        logger.setLevel(log_level)

        # ========================================================
        # Create StreamHandler with unified format
        # ========================================================
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)

        # ========================================================
        # Attach handler to logger
        # ========================================================
        logger.addHandler(handler)

    return logger
