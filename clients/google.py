"""Google OAuth client."""
from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from fastapi_oauth20 import GoogleOAuth20, FastAPIOAuth20

from config import settings

router = APIRouter()

# Initialize Google OAuth client
google_client = None
redirect_uri = f"{settings.app_url}/api/v1/oauth2/google/callback"

if settings.google_client_id and settings.google_client_secret:
    google_client = GoogleOAuth20(
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
    )


@router.get("/api/v1/oauth2/google/authorize")
async def google_auth():
    """Initiate Google OAuth login."""
    if not google_client:
        return RedirectResponse(url="/?error=provider_not_supported")

    auth_url = await google_client.get_authorization_url(redirect_uri=redirect_uri)
    return RedirectResponse(url=auth_url)


@router.get("/api/v1/oauth2/google/callback")
async def google_callback(
    request: Request,
    oauth2: Annotated[
        FastAPIOAuth20,
        Depends(FastAPIOAuth20(google_client, redirect_uri=redirect_uri)),
    ],
):
    """Handle Google OAuth callback."""
    if not google_client:
        return RedirectResponse(url="/?error=provider_not_supported")

    try:
        token_data, state = oauth2
        access_token = token_data['access_token']
        user_info = await google_client.get_userinfo(access_token)

        # Store user in session
        request.session["user"] = {
            "provider": "google",
            "data": user_info,
        }

        return RedirectResponse(url="/")
    except Exception as e:
        error_msg = str(e)
        print(f"Google OAuth error: {error_msg}")
        return RedirectResponse(url=f"/?error=oauth_failed&provider=google&details={error_msg[:100]}")
