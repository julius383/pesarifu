from pathlib import Path

from dotenv import dotenv_values, find_dotenv

ROOT_DIR: Path = Path(find_dotenv(".env")).absolute().parent
STATEMENTS_BASE_DIR = ROOT_DIR / "uploads"
EXPORTS_BASE_DIR = ROOT_DIR / "exports"
APP_BASE_URL = "https://app.pesarifu.com/"
CONFIG: dict[str, str | None] = dotenv_values()
