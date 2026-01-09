from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    # Application
    app_name: str = "FastAPI OAuth20 Demo"
    app_url: str = "http://127.0.0.1:8000"

    # GitHub OAuth
    github_client_id: str
    github_client_secret: str

    # Google OAuth
    google_client_id: str
    google_client_secret: str

    # FeiShu OAuth
    feishu_client_id: str
    feishu_client_secret: str

    # Gitee OAuth
    gitee_client_id: str
    gitee_client_secret: str

    # Linux.do OAuth
    linuxdo_client_id: str
    linuxdo_client_secret: str

    # OSChina OAuth
    oschina_client_id: str
    oschina_client_secret: str

    # WeChat Mini Program OAuth
    wechat_mp_client_id: str
    wechat_mp_client_secret: str

    # WeChat Open Platform OAuth
    wechat_open_client_id: str
    wechat_open_client_secret: str


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
