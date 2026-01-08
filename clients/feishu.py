"""FeiShu OAuth client."""
from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from fastapi_oauth20 import FeiShuOAuth20, FastAPIOAuth20

from config import settings

router = APIRouter()

# Initialize FeiShu OAuth client
feishu_client = None
redirect_uri = f"{settings.app_url}/api/v1/oauth2/feishu/callback"

if settings.feishu_client_id and settings.feishu_client_secret:
    feishu_client = FeiShuOAuth20(
        client_id=settings.feishu_client_id,
        client_secret=settings.feishu_client_secret,
    )


@router.get("/api/v1/oauth2/feishu/authorize")
async def feishu_auth():
    """Initiate FeiShu OAuth login."""
    if not feishu_client:
        return RedirectResponse(url="/?error=provider_not_supported")

    auth_url = await feishu_client.get_authorization_url(redirect_uri=redirect_uri)
    return RedirectResponse(url=auth_url)


@router.get("/api/v1/oauth2/feishu/callback")
async def feishu_callback(
    request: Request,
    oauth2: Annotated[
        FastAPIOAuth20,
        Depends(FastAPIOAuth20(feishu_client, redirect_uri=redirect_uri)),
    ],
):
    """Handle FeiShu OAuth callback."""
    if not feishu_client:
        return RedirectResponse(url="/?error=provider_not_supported")

    try:
        token_data, state = oauth2
        access_token = token_data['access_token']
        user_info = await feishu_client.get_userinfo(access_token)

        # Store user in session
        request.session["user"] = {
            "provider": "feishu",
            "data": user_info,
        }

        return RedirectResponse(url="/")
    except Exception as e:
        error_msg = str(e)
        print(f"FeiShu OAuth error: {error_msg}")
        return RedirectResponse(url=f"/?error=oauth_failed&provider=feishu&details={error_msg[:100]}")
