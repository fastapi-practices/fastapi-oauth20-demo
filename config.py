from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # Application
    APP_NAME: str = "FastAPI OAuth20 Demo"
    APP_URL: str = "http://127.0.0.1:8000"

    # GitHub OAuth
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    GITHUB_REDIRECT_URI: str = "http://127.0.0.1:8000/api/v1/oauth2/github/callback"

    # Google OAuth
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str = "http://127.0.0.1:8000/api/v1/oauth2/google/callback"

    # FeiShu OAuth
    FEISHU_CLIENT_ID: str
    FEISHU_CLIENT_SECRET: str
    FEISHU_REDIRECT_URI: str = "http://127.0.0.1:8000/api/v1/oauth2/feishu/callback"

    # Gitee OAuth
    GITEE_CLIENT_ID: str
    GITEE_CLIENT_SECRET: str
    GITEE_REDIRECT_URI: str = "http://127.0.0.1:8000/api/v1/oauth2/gitee/callback"

    # Linux.do OAuth
    LINUXDO_CLIENT_ID: str
    LINUXDO_CLIENT_SECRET: str
    LINUXDO_REDIRECT_URI: str = "http://127.0.0.1:8000/api/v1/oauth2/linux-do/callback"

    # OSChina OAuth
    OSCHINA_CLIENT_ID: str
    OSCHINA_CLIENT_SECRET: str
    OSCHINA_REDIRECT_URI: str = "http://127.0.0.1:8000/api/v1/oauth2/oschina/callback"

    # WeChat Mini Program OAuth
    WECHAT_MP_CLIENT_ID: str
    WECHAT_MP_CLIENT_SECRET: str
    WECHAT_MP_REDIRECT_URI: str = "http://127.0.0.1:8000/api/v1/oauth2/wechat_mp/callback"

    # WeChat Open Platform OAuth
    WECHAT_OPEN_CLIENT_ID: str
    WECHAT_OPEN_CLIENT_SECRET: str
    WECHAT_OPEN_REDIRECT_URI: str = "http://127.0.0.1:8000/api/v1/oauth2/wechat_open/callback"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
