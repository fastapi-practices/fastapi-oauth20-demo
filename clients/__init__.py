"""OAuth clients module."""
from .github import router as github_router
from .google import router as google_router
from .feishu import router as feishu_router
from .gitee import router as gitee_router
from .linuxdo import router as linuxdo_router
from .oschina import router as oschina_router

__all__ = [
    "github_router",
    "google_router",
    "feishu_router",
    "gitee_router",
    "linuxdo_router",
    "oschina_router",
]
