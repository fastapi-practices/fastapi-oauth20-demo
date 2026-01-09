from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from clients import (
    github_router,
    google_router,
    feishu_router,
    gitee_router,
    linuxdo_router,
    oschina_router,
    wechat_mp_router,
    wechat_open_router,
)
from config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager."""
    yield


# Create FastAPI app
app = FastAPI(
    title="FastAPI OAuth20 Demo",
    description="Demo application showing OAuth2 integration with multiple providers",
    version="0.0.1",
    lifespan=lifespan,
)

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key="change-this-in-production",
    max_age=3600,
)

# Include OAuth client routers
app.include_router(github_router, tags=["GitHub OAuth"])
app.include_router(google_router, tags=["Google OAuth"])
app.include_router(feishu_router, tags=["FeiShu OAuth"])
app.include_router(gitee_router, tags=["Gitee OAuth"])
app.include_router(linuxdo_router, tags=["LinuxDo OAuth"])
app.include_router(oschina_router, tags=["OSChina OAuth"])
app.include_router(wechat_mp_router, tags=["WeChat MP OAuth"])
app.include_router(wechat_open_router, tags=["WeChat Open OAuth"])

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_enabled_providers() -> dict[str, bool]:
    """Get dictionary of enabled OAuth providers."""
    return {
        "github": bool(settings.github_client_id and settings.github_client_secret),
        "google": bool(settings.google_client_id and settings.google_client_secret),
        "feishu": bool(settings.feishu_client_id and settings.feishu_client_secret),
        "gitee": bool(settings.gitee_client_id and settings.gitee_client_secret),
        "linuxdo": bool(settings.linuxdo_client_id and settings.linuxdo_client_secret),
        "oschina": bool(settings.oschina_client_id and settings.oschina_client_secret),
        "wechat_mp": bool(settings.wechat_mp_client_id and settings.wechat_mp_client_secret),
        "wechat_open": bool(settings.wechat_open_client_id and settings.wechat_open_client_secret),
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """Home page with login buttons."""
    providers = {k: v for k, v in get_enabled_providers().items() if v}
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "providers": providers,
            "user": request.session.get("user"),
        },
    )


@app.get("/logout")
async def logout(request: Request) -> RedirectResponse:
    """Log out the current user."""
    request.session.clear()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/api/user")
async def get_user(request: Request) -> JSONResponse:
    """Get current user info as JSON."""
    user = request.session.get("user")
    if not user:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "Not authenticated"},
        )
    return JSONResponse(content=user)


@app.get("/api/providers")
async def get_providers() -> JSONResponse:
    """Get list of available OAuth providers."""
    providers = get_enabled_providers()
    enabled = [k for k, v in providers.items() if v]
    return JSONResponse(
        content={
            "providers": enabled,
            "count": len(enabled),
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": str(exc)},
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
