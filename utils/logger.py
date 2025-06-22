import logging
import os

from config.logging import setup_logging


def get_logger(obj_or_name) -> logging.Logger:
    setup_logging()

    if isinstance(obj_or_name, str):
        parts = obj_or_name.replace(".", "/").split("/")
        class_name = None
    else:
        parts = obj_or_name.__module__.split(".")
        class_name = obj_or_name.__class__.__name__

    if class_name:
        parts.append(class_name)

    logger_name = f"[{'|'.join(parts)}]"
    return logging.getLogger(logger_name)
