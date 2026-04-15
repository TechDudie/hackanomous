from fastapi import APIRouter
from fastapi.responses import JSONResponse
import os
from urllib.parse import quote

from app.config import config

BASE_URL = os.getenv("HACKANOMOUS_BASE_URL", "http://localhost:8080" if os.getenv("HACKANOMOUS_DEVELOPMENT", "0") == "1" else (config.get("base_url") or "https://hackanomous.hackclub.com")) # TODO: prod url?

HACKCLUB_CLIENT_ID = config.get("oauth.hackclub.client_id")
HACKCLUB_SECRET = config.get("oauth.hackclub.secret")
HACKCLUB_REDIRECT_URI = f"{BASE_URL}/oauth/hackclub/callback"
HACKCLUB_RESPONSE_TYPE = "code"
HACKCLUB_SCOPES = ["openid", "email", "name", "profile", "verification_status", "slack_id"]

HACKATIME_CLIENT_ID = config.get("oauth.hackatime.client_id")
HACKATIME_SECRET = config.get("oauth.hackatime.secret")
HACKATIME_REDIRECT_URI = f"{BASE_URL}/oauth/hackatime/callback"
HACKATIME_RESPONSE_TYPE = "code"
HACKATIME_SCOPES = ["profile", "read"]

required = [
    ("oauth.hackclub.client_id", HACKCLUB_CLIENT_ID),
    ("oauth.hackclub.secret", HACKCLUB_SECRET),
    ("oauth.hackatime.client_id", HACKATIME_CLIENT_ID),
    ("oauth.hackatime.secret", HACKATIME_SECRET),
]

for k, v in required:
    if not v:
        raise ValueError(f"Missing required configuration: {k}")

HACKCLUB_OAUTH_URL = f"https://auth.hackclub.com/oauth/authorize?client_id={quote(HACKCLUB_CLIENT_ID)}&redirect_uri={quote(HACKCLUB_REDIRECT_URI)}&response_type={quote(HACKCLUB_RESPONSE_TYPE)}&scope={'+'.join(HACKCLUB_SCOPES)}"
HACKATIME_OAUTH_URL = f"https://hackatime.hackclub.com/oauth/authorize?client_id={quote(HACKATIME_CLIENT_ID)}&redirect_uri={quote(HACKATIME_REDIRECT_URI)}&response_type={quote(HACKATIME_RESPONSE_TYPE)}&scope={'+'.join(HACKATIME_SCOPES)}"

# /api/v1/oauth is prefix for non callback oauth routes (like getting ts oauth urls)
oauth = APIRouter()

@oauth.get("/hackclub/url")
async def get_hackclub_oauth_url():
    return JSONResponse(
        status_code=200,
        content={"message": "url generated successfully", "url": HACKCLUB_OAUTH_URL}
    )

@oauth.get("/hackatime/url")
async def get_hackatime_oauth_url():
    return JSONResponse(
        status_code=200,
        content={"message": "url generated successfully", "url": HACKATIME_OAUTH_URL}
    )

# /oauth is prefix for all callback routes
callbacks = APIRouter()

HACKCLUB = APIRouter()

@HACKCLUB.get("/callback")
async def hackclub_callback():
    return JSONResponse(
        status_code=200,
        content={"message": "callback world"}
    )

callbacks.include_router(HACKCLUB, prefix="/hackclub")

HACKATIME = APIRouter()

@HACKATIME.get("/callback")
async def hackatime_callback():
    return JSONResponse(
        status_code=200,
        content={"message": "callback world"}
    )

callbacks.include_router(HACKATIME, prefix="/hackatime")
