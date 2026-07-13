import os
import platform
import sys
from datetime import datetime

if platform.system() == "Windows":
    path_divider = "\\"
else:
    path_divider = "/"

ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, "Config")
DATA_FILES_PATH = os.path.join(ROOT_DIR, "test_data")
SCREENSHOT_PATH = os.path.join(ROOT_DIR, f"Artifacts{path_divider}Screenshots")
LOGS_PATH = os.path.join(ROOT_DIR, f"Artifacts{path_divider}Logs")
VIDEO_DIR = os.path.join(ROOT_DIR, f"Artifacts{path_divider}Videos")
DOWNLOADS_PATH = os.path.join(ROOT_DIR, f"Artifacts{path_divider}Downloads")
PROD_DOWNLOAD_PATH = os.path.join(ROOT_DIR, f"Artifacts{path_divider}Downloads")


def get_current_project(default="lct"):
    project = os.getenv("PROJECT")
    if project:
        return project.lower()

    for index, arg in enumerate(sys.argv):
        if arg == "--project" and index + 1 < len(sys.argv):
            return sys.argv[index + 1].lower()
        if arg.startswith("--project="):
            return arg.split("=", 1)[1].lower()

    return default


_ARTIFACT_RUN_ID = os.getenv("ARTIFACT_RUN_ID")


def get_artifact_run_id():
    global _ARTIFACT_RUN_ID
    if _ARTIFACT_RUN_ID:
        return _ARTIFACT_RUN_ID

    _ARTIFACT_RUN_ID = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    _ARTIFACT_RUN_ID = f"{_ARTIFACT_RUN_ID}_pid-{os.getpid()}"
    return _ARTIFACT_RUN_ID


def get_project_logs_path(project=None, run_id=None):
    return os.path.join(
        LOGS_PATH,
        project or get_current_project(),
        run_id or get_artifact_run_id(),
    )


def get_project_screenshot_path(project=None, run_id=None):
    return os.path.join(
        SCREENSHOT_PATH,
        project or get_current_project(),
        run_id or get_artifact_run_id(),
    )
