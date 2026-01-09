"""GitHub OAuth client."""
from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from fastapi_oauth20 import GitHubOAuth20, FastAPIOAuth20

from config import settings

router = APIRouter()

# Initialize GitHub OAuth client
github_client = None

if settings.GITHUB_CLIENT_ID and settings.GITHUB_CLIENT_SECRET:
    github_client = GitHubOAuth20(
        client_id=settings.GITHUB_CLIENT_ID,
        client_secret=settings.GITHUB_CLIENT_SECRET,
    )


@router.get("/api/v1/oauth2/github/authorize")
async def github_auth():
    """Initiate GitHub OAuth login."""
    if not github_client:
        return RedirectResponse(url="/?error=provider_not_supported")

    auth_url = await github_client.get_authorization_url(redirect_uri=settings.GITHUB_REDIRECT_URI)
    return RedirectResponse(url=auth_url)


@router.get("/api/v1/oauth2/github/callback")
async def github_callback(
    request: Request,
    oauth2: Annotated[
        FastAPIOAuth20,
        Depends(FastAPIOAuth20(github_client, redirect_uri=settings.GITHUB_REDIRECT_URI)),
    ],
):
    """Handle GitHub OAuth callback."""
    if not github_client:
        return RedirectResponse(url="/?error=provider_not_supported")

    try:
        token_data, state = oauth2
        access_token = token_data['access_token']
        user_info = await github_client.get_userinfo(access_token)

        # Store user in session
        request.session["user"] = {
            "provider": "github",
            "data": user_info,
        }

        return RedirectResponse(url="/")
    except Exception as e:
        error_msg = str(e)
        print(f"GitHub OAuth error: {error_msg}")
        return RedirectResponse(url=f"/?error=oauth_failed&provider=github&details={error_msg[:100]}")
