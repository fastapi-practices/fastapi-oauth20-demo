"""OSChina OAuth client."""
from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from fastapi_oauth20 import OSChinaOAuth20, FastAPIOAuth20

from config import settings

router = APIRouter()

# Initialize OSChina OAuth client
oschina_client = None

if settings.OSCHINA_CLIENT_ID and settings.OSCHINA_CLIENT_SECRET:
    oschina_client = OSChinaOAuth20(
        client_id=settings.OSCHINA_CLIENT_ID,
        client_secret=settings.OSCHINA_CLIENT_SECRET,
    )


@router.get("/api/v1/oauth2/oschina/authorize")
async def oschina_auth():
    """Initiate OSChina OAuth login."""
    if not oschina_client:
        return RedirectResponse(url="/?error=provider_not_supported")

    auth_url = await oschina_client.get_authorization_url(redirect_uri=settings.OSCHINA_REDIRECT_URI)
    return RedirectResponse(url=auth_url)


@router.get("/api/v1/oauth2/oschina/callback")
async def oschina_callback(
    request: Request,
    oauth2: Annotated[
        FastAPIOAuth20,
        Depends(FastAPIOAuth20(oschina_client, redirect_uri=settings.OSCHINA_REDIRECT_URI)),
    ],
):
    """Handle OSChina OAuth callback."""
    if not oschina_client:
        return RedirectResponse(url="/?error=provider_not_supported")

    try:
        token_data, state = oauth2
        access_token = token_data['access_token']
        user_info = await oschina_client.get_userinfo(access_token)

        # Store user in session
        request.session["user"] = {
            "provider": "oschina",
            "data": user_info,
        }

        return RedirectResponse(url="/")
    except Exception as e:
        error_msg = str(e)
        print(f"OSChina OAuth error: {error_msg}")
        return RedirectResponse(url=f"/?error=oauth_failed&provider=oschina&details={error_msg[:100]}")
