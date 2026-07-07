import logging
import os
from pathlib import Path

from config.global_var import (
    get_artifact_run_id,
    get_current_project,
    get_project_logs_path,
)


def _ensure_log_dir():
    """Create logs directory if not present."""
    logs_path = get_project_logs_path()
    if not os.path.isdir(logs_path):
        os.makedirs(logs_path, exist_ok=True)


def _suite_log_name() -> str:
    """Generate suite log file name."""
    suite_name = os.getenv("SUITE_NAME", "lct")
    project = get_current_project()
    run_id = get_artifact_run_id()
    return f"{project}_{suite_name}_{run_id}.log"


_LOG_FILE_PATH: Path | None = None
_FILE_HANDLER: logging.FileHandler | None = None
_CONSOLE_HANDLER: logging.StreamHandler | None = None
_FORMATTER = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")


def _get_log_file_path() -> Path:
    """Return single log file path for entire execution."""
    global _LOG_FILE_PATH

    if _LOG_FILE_PATH is None:
        _ensure_log_dir()
        _LOG_FILE_PATH = Path(get_project_logs_path()) / _suite_log_name()

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
