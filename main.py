import json
import os
from urllib.parse import quote_plus, urlencode

import uvicorn
from authlib.integrations.starlette_client import OAuth
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

load_dotenv()

token_auth_scheme = HTTPBearer()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
AUTH0_SESSION_SECRET = os.getenv("SECRET_KEY")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(SessionMiddleware, secret_key=AUTH0_SESSION_SECRET)


oauth = OAuth()
oauth.register(
    "auth0",
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def ProtectedEndpoint(request: Request):
    if not "id_token" in request.session:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail="Not authorized",
            headers={"Location": "/login"},
        )


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/profile", dependencies=[Depends(ProtectedEndpoint)])
def profile(request: Request):
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "userinfo": request.session["userinfo"],
            "formatted_userinfo": json.dumps(
                request.session["userinfo"], default=lambda o: o.__dict__, indent=4
            ),
        },
    )


@app.get("/login")
async def login(request: Request):
    if not "id_token" in request.session:
        return await oauth.auth0.authorize_redirect(
            request,
            redirect_uri="http://127.0.0.1:8000/callback",
            audience=AUTH0_AUDIENCE,
        )
    return RedirectResponse(url="/")


@app.get("/logout")
def logout(request: Request):
    response = RedirectResponse(
        url="https://"
        + AUTH0_DOMAIN
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri("home"),
                "client_id": AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )
    request.session.clear()
    return response


@app.route("/callback", methods=["GET", "POST"])
async def callback(request: Request):
    """
    Callback redirect from Auth0
    """
    token = await oauth.auth0.authorize_access_token(request)
    request.session["access_token"] = token["access_token"]
    request.session["id_token"] = token["id_token"]
    request.session["userinfo"] = token["userinfo"]
    return RedirectResponse(url=app.url_path_for("profile"))


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
