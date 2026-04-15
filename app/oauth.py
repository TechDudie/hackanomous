from datetime import datetime, timedelta
import os
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import httpx
import jwt
from sqlmodel import select

from app.config import config
from app.database import SessionLocal, User

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

try:
    ssh = os.path.expanduser("~/.ssh")
    with open(os.path.join(ssh, "id_rsa.pub"), "r") as f:
        RSA_PUBLIC_KEY = f.read()
    with open(os.path.join(ssh, "id_rsa"), "r") as f:
        RSA_PRIVATE_KEY = f.read()
except FileNotFoundError:
    raise ValueError("Missing RSA key pair at ~/.ssh/")

bearer = HTTPBearer(auto_error=True)

# TODO: rework this to be more relevant
def get_auth_payload(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> dict[str, object]:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(401, "missing or invalid authorization")

    try:
        payload = jwt.decode(credentials.credentials, RSA_PUBLIC_KEY, algorithms=["RS256"])
    except jwt.InvalidTokenError:
        raise HTTPException(401, "invalid or expired token")

    uid = payload.get("id")
    if not isinstance(uid, str):
        raise HTTPException(401, "invalid token payload")

    return payload

# TODO: idfk just seems lil sketchy
def generate_jwt_token(id: str) -> str:
    token = jwt.encode(
        {
            "id": id,
            "exp": int((datetime.now() + timedelta(weeks=1)).timestamp()),  # TODO: adjust as needed
        },
        RSA_PRIVATE_KEY,
        algorithm="RS256",
    )
    return token

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
async def hackclub_callback(code: str):
    async with httpx.AsyncClient() as s:
        r = await s.post(
            "https://auth.hackclub.com/oauth/token",
            data={
                "client_id": HACKCLUB_CLIENT_ID,
                "client_secret": HACKCLUB_SECRET,
                "redirect_uri": HACKCLUB_REDIRECT_URI,
                "code": code,
                "grant_type": "authorization_code",
            }
        )
        r.raise_for_status()
        oauth_response = r.json()
        authorization = oauth_response.get("token_type", "Bearer") + " " + oauth_response.get("access_token", "")

        r = await s.get(
            "https://auth.hackclub.com/api/v1/me",
            headers={"Authorization": authorization}
        )
        r.raise_for_status()
        identity_response = r.json()
        identity = identity_response.get("identity", {})
        user_id = identity.get("id")

        if user_id is None:
            return JSONResponse(
                status_code=400,
                content={"message": "hackclub identity id missing from response"},
            )

        user_id = str(user_id)

        async with SessionLocal() as db:
            result = await db.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()

            if user is None:
                user = User(
                    id=user_id,
                    hackclub_oauth_response=oauth_response,
                    hackclub_authorization=authorization,
                    identity=identity,
                )
                db.add(user)
            else:
                user.hackclub_oauth_response = oauth_response
                user.hackclub_authorization = authorization
                user.identity = identity

            await db.commit()

    token = generate_jwt_token(user_id)
    response = RedirectResponse(url=BASE_URL, status_code=302)
    response.set_cookie(key="_jwt_session_token", value=token)
    return response

callbacks.include_router(HACKCLUB, prefix="/hackclub")

HACKATIME = APIRouter()

@HACKATIME.get("/callback")
async def hackatime_callback():
    return JSONResponse(
        status_code=200,
        content={"message": "callback world"}
    )

callbacks.include_router(HACKATIME, prefix="/hackatime")
