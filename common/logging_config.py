# common/logging_config.py

import logging
import os


def get_logger(name: str) -> logging.Logger:
    """
    Retorna un logger configurado con formato unificado para todo el proyecto.

    - Nivel por defecto: INFO
    - Respeta la variable de entorno LOG_LEVEL si está definida.
    - Evita agregar handlers duplicados si se solicita el mismo logger varias veces.
    """

    logger = logging.getLogger(name)

    if not logger.handlers:
        # Nivel dinámico (LOG_LEVEL), con fallback en INFO
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        logger.setLevel(log_level)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    return logger
