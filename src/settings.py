from pathlib import Path

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding='utf-8',
        case_sensitive=True,
    )

    # DB
    DATABASE_URL: str = ''

    # Meta / Graph
    META_ACCESS_TOKEN: str = ''
    META_AD_ACCOUNT_ID: str = ''  # act_<id>
    META_GRAPH_BASE: str = 'https://graph.facebook.com'
    META_GRAPH_VERSION: str = 'v23.0'
    META_CREATIVE_ID: str = ''
    META_PAGE_ACCESS_TOKEN: str = ''
    META_POST_ID: str = ''

    REQUEST_TIMEOUT_SEC: int = 30

    # CSV
    CSV_DIR: Path = PROJECT_ROOT / 'data'

settings = Settings()
