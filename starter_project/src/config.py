from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
ENV_FILE = PROJECT_ROOT / ".env"

PASSED_DATASET = DATA_DIR / "orders_passed.csv"
FAILED_DATASET = DATA_DIR / "orders_failed.csv"
SUMMARY_FILE = OUTPUT_DIR / "validation_summary.json"

VALID_STATUSES = {"completed", "pending", "cancelled"}


def load_env_file(env_file: Path = ENV_FILE) -> None:
    if not env_file.exists():
        return

    for line in env_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue

        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file()

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")


def resolve_project_path(raw_path: str | os.PathLike[str]) -> Path:
    path = Path(raw_path).expanduser()
    if path.is_absolute():
        return path
    return PROJECT_ROOT / path


AIRFLOW_INPUT_FILE = resolve_project_path(os.getenv("AIRFLOW_INPUT_FILE", str(PASSED_DATASET)))
