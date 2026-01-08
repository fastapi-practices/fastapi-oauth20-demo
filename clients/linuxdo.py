"""LinuxDo OAuth client."""
from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from fastapi_oauth20 import LinuxDoOAuth20, FastAPIOAuth20

from config import settings

router = APIRouter()

# Initialize LinuxDo OAuth client
linuxdo_client = None
redirect_uri = f"{settings.app_url}/api/v1/oauth2/linux-do/callback"

if settings.linuxdo_client_id and settings.linuxdo_client_secret:
    linuxdo_client = LinuxDoOAuth20(
        client_id=settings.linuxdo_client_id,
        client_secret=settings.linuxdo_client_secret,
    )


@router.get("/api/v1/oauth2/linux-do/authorize")
async def linuxdo_auth():
    """Initiate LinuxDo OAuth login."""
    if not linuxdo_client:
        return RedirectResponse(url="/?error=provider_not_supported")

    auth_url = await linuxdo_client.get_authorization_url(redirect_uri=redirect_uri)
    return RedirectResponse(url=auth_url)


@router.get("/api/v1/oauth2/linux-do/callback")
async def linuxdo_callback(
    request: Request,
    oauth2: Annotated[
        FastAPIOAuth20,
        Depends(FastAPIOAuth20(linuxdo_client, redirect_uri=redirect_uri)),
    ],
):
    """Handle LinuxDo OAuth callback."""
    if not linuxdo_client:
        return RedirectResponse(url="/?error=provider_not_supported")

    try:
        token_data, state = oauth2
        access_token = token_data['access_token']
        user_info = await linuxdo_client.get_userinfo(access_token)

        # Store user in session
        request.session["user"] = {
            "provider": "linuxdo",
            "data": user_info,
        }

        return RedirectResponse(url="/")
    except Exception as e:
        error_msg = str(e)
        print(f"LinuxDo OAuth error: {error_msg}")
        return RedirectResponse(url=f"/?error=oauth_failed&provider=linuxdo&details={error_msg[:100]}")
