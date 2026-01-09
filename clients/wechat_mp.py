"""WeChat Mini Program OAuth client."""
from typing import Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from fastapi_oauth20 import WeChatMpOAuth20, FastAPIOAuth20

from config import settings

router = APIRouter()

# Initialize WeChat Mini Program OAuth client
wechat_mp_client = None
redirect_uri = f"{settings.app_url}/api/v1/oauth2/wechat_mp/callback"

if settings.wechat_mp_client_id and settings.wechat_mp_client_secret:
    wechat_mp_client = WeChatMpOAuth20(
        client_id=settings.wechat_mp_client_id,
        client_secret=settings.wechat_mp_client_secret,
    )


@router.get("/api/v1/oauth2/wechat_mp/authorize")
async def wechat_mp_auth():
    """Initiate WeChat Mini Program OAuth login."""
    if not wechat_mp_client:
        return RedirectResponse(url="/?error=provider_not_supported")

    auth_url = await wechat_mp_client.get_authorization_url(redirect_uri=redirect_uri)
    return RedirectResponse(url=auth_url)


@router.get("/api/v1/oauth2/wechat_mp/callback")
async def wechat_mp_callback(
    request: Request,
    oauth2: Annotated[
        FastAPIOAuth20,
        Depends(FastAPIOAuth20(wechat_mp_client, redirect_uri=redirect_uri)),
    ],
):
    """Handle WeChat Mini Program OAuth callback."""
    if not wechat_mp_client:
        return RedirectResponse(url="/?error=provider_not_supported")

    try:
        token_data, state = oauth2
        access_token = token_data['access_token']
        openid = token_data['openid']
        user_info = await wechat_mp_client.get_userinfo(access_token, openid)

        # Store user in session
        request.session["user"] = {
            "provider": "wechat_mp",
            "data": user_info,
        }

        return RedirectResponse(url="/")
    except Exception as e:
        error_msg = str(e)
        print(f"WeChat Mini Program OAuth error: {error_msg}")
        return RedirectResponse(url=f"/?error=oauth_failed&provider=wechat_mp&details={error_msg[:100]}")
