"""Gitee OAuth client."""
from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from fastapi_oauth20 import GiteeOAuth20, FastAPIOAuth20

from config import settings

router = APIRouter()

# Initialize Gitee OAuth client
gitee_client = None

if settings.GITEE_CLIENT_ID and settings.GITEE_CLIENT_SECRET:
    gitee_client = GiteeOAuth20(
        client_id=settings.GITEE_CLIENT_ID,
        client_secret=settings.GITEE_CLIENT_SECRET,
    )


@router.get("/api/v1/oauth2/gitee/authorize")
async def gitee_auth():
    """Initiate Gitee OAuth login."""
    if not gitee_client:
        return RedirectResponse(url="/?error=provider_not_supported")

    auth_url = await gitee_client.get_authorization_url(redirect_uri=settings.GITEE_REDIRECT_URI)
    return RedirectResponse(url=auth_url)


@router.get("/api/v1/oauth2/gitee/callback")
async def gitee_callback(
    request: Request,
    oauth2: Annotated[
        FastAPIOAuth20,
        Depends(FastAPIOAuth20(gitee_client, redirect_uri=settings.GITEE_REDIRECT_URI)),
    ],
):
    """Handle Gitee OAuth callback."""
    if not gitee_client:
        return RedirectResponse(url="/?error=provider_not_supported")

    try:
        token_data, state = oauth2
        access_token = token_data['access_token']
        user_info = await gitee_client.get_userinfo(access_token)

        # Store user in session
        request.session["user"] = {
            "provider": "gitee",
            "data": user_info,
        }

        return RedirectResponse(url="/")
    except Exception as e:
        error_msg = str(e)
        print(f"Gitee OAuth error: {error_msg}")
        return RedirectResponse(url=f"/?error=oauth_failed&provider=gitee&details={error_msg[:100]}")
