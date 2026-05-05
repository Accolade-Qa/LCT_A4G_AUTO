import logging
import os
from datetime import datetime
from pathlib import Path

from config.global_var import LOGS_PATH


def _ensure_log_dir():
    if not os.path.isdir(LOGS_PATH):
        os.makedirs(LOGS_PATH, exist_ok=True)


def _suite_log_name() -> str:
    suite_name = os.getenv("SUITE_NAME", "LCT_A4G_AUTO")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{suite_name}_{timestamp}.log"


_LOG_FILE_PATH: Path | None = None


def _get_log_file_path() -> Path:
    global _LOG_FILE_PATH
    if _LOG_FILE_PATH is None:
        _ensure_log_dir()
        _LOG_FILE_PATH = Path(LOGS_PATH) / _suite_log_name()
    return _LOG_FILE_PATH


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger instance.

    Logs travel to console and a suite-specific file inside Artifacts/Logs.
    """
    _ensure_log_dir()
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_path = _get_log_file_path()
    file_handler = logging.FileHandler(file_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.propagate = False

    return logger
