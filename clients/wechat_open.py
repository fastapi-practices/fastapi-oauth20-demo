"""WeChat Open Platform OAuth client."""
from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from fastapi_oauth20 import WeChatOpenOAuth20, FastAPIOAuth20

from config import settings

router = APIRouter()

# Initialize WeChat Open Platform OAuth client
wechat_open_client = None

if settings.WECHAT_OPEN_CLIENT_ID and settings.WECHAT_OPEN_CLIENT_SECRET:
    wechat_open_client = WeChatOpenOAuth20(
        client_id=settings.WECHAT_OPEN_CLIENT_ID,
        client_secret=settings.WECHAT_OPEN_CLIENT_SECRET,
    )


@router.get("/api/v1/oauth2/wechat_open/authorize")
async def wechat_open_auth():
    """Initiate WeChat Open Platform OAuth login."""
    if not wechat_open_client:
        return RedirectResponse(url="/?error=provider_not_supported")

    auth_url = await wechat_open_client.get_authorization_url(redirect_uri=settings.WECHAT_OPEN_REDIRECT_URI)
    return RedirectResponse(url=auth_url)


@router.get("/api/v1/oauth2/wechat_open/callback")
async def wechat_open_callback(
    request: Request,
    oauth2: Annotated[
        FastAPIOAuth20,
        Depends(FastAPIOAuth20(wechat_open_client, redirect_uri=settings.WECHAT_OPEN_REDIRECT_URI)),
    ],
):
    """Handle WeChat Open Platform OAuth callback."""
    if not wechat_open_client:
        return RedirectResponse(url="/?error=provider_not_supported")

    try:
        token_data, state = oauth2
        access_token = token_data['access_token']
        openid = token_data['openid']
        user_info = await wechat_open_client.get_userinfo(access_token, openid)

        # Store user in session
        request.session["user"] = {
            "provider": "wechat_open",
            "data": user_info,
        }

        return RedirectResponse(url="/")
    except Exception as e:
        error_msg = str(e)
        print(f"WeChat Open Platform OAuth error: {error_msg}")
        return RedirectResponse(url=f"/?error=oauth_failed&provider=wechat_open&details={error_msg[:100]}")
