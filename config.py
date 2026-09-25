from dataclasses import dataclass
from pathlib import Path
import os

@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("ORANGEHRM_BASE_URL", "https://opensource-demo.orangehrmlive.com")
    username: str = os.getenv("ORANGEHRM_USERNAME", "Admin")
    password: str = os.getenv("ORANGEHRM_PASSWORD", "admin123")
    headless: bool = os.getenv("HEADLESS", "true").lower() == "true"
    timeout: int = int(os.getenv("SELENIUM_TIMEOUT", "20"))
    artifact_dir: Path = Path(os.getenv("ARTIFACT_DIR", "reports"))
    api_base_url: str = os.getenv("MOCK_API_URL", "https://api.restful-api.dev")
    record_video: bool = os.getenv("RECORD_VIDEO", "false").lower() == "true"

settings = Settings()
