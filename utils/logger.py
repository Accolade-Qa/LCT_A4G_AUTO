import logging
import os
from datetime import datetime
from pathlib import Path

from config.global_var import LOGS_PATH


def _ensure_log_dir():
    """Create logs directory if not present."""
    if not os.path.isdir(LOGS_PATH):
        os.makedirs(LOGS_PATH, exist_ok=True)


def _suite_log_name() -> str:
    """Generate suite log file name."""
    suite_name = os.getenv("SUITE_NAME", "LCT_A4G_AUTO")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return f"{suite_name}_{timestamp}.log"


_LOG_FILE_PATH: Path | None = None
_FILE_HANDLER: logging.FileHandler | None = None
_CONSOLE_HANDLER: logging.StreamHandler | None = None
_FORMATTER = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")


def _get_log_file_path() -> Path:
    """Return single log file path for entire execution."""
    global _LOG_FILE_PATH

    if _LOG_FILE_PATH is None:
        _ensure_log_dir()
        _LOG_FILE_PATH = Path(LOGS_PATH) / _suite_log_name()

    return _LOG_FILE_PATH


def get_logger(name: str) -> logging.Logger:
    """
    Return configured logger instance.
    Prevents duplicate handlers.
    """

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    global _FILE_HANDLER, _CONSOLE_HANDLER

    # File handler is delayed so imports/collection do not create empty log files.
    if _FILE_HANDLER is None:
        _FILE_HANDLER = logging.FileHandler(
            _get_log_file_path(), encoding="utf-8", delay=True
        )
        _FILE_HANDLER.setLevel(logging.DEBUG)
        _FILE_HANDLER.setFormatter(_FORMATTER)

    if _CONSOLE_HANDLER is None:
        _CONSOLE_HANDLER = logging.StreamHandler()
        _CONSOLE_HANDLER.setLevel(logging.INFO)
        _CONSOLE_HANDLER.setFormatter(_FORMATTER)

    logger.addHandler(_FILE_HANDLER)
    logger.addHandler(_CONSOLE_HANDLER)

    return logger
