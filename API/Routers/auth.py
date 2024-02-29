from urllib.parse import quote_plus, urlencode

from authlib.integrations.starlette_client import OAuth
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, RedirectResponse

import settings

router = APIRouter()

oauth = OAuth()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)


def ProtectedEndpoint(request: Request):
    if not "id_token" in request.session:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail="Not authorized",
            headers={"Location": "/login"},
        )


@router.get("/")
def home(request: Request):
    return JSONResponse({"message": "Index page"})


@router.get("/profile", dependencies=[Depends(ProtectedEndpoint)])
def profile(request: Request):
    user_data = jsonable_encoder(request.session["userinfo"])
    return JSONResponse(content=user_data)


@router.get("/login")
async def login(request: Request):
    if not "id_token" in request.session:
        return await oauth.auth0.authorize_redirect(
            request,
            redirect_uri=settings.AUTH0_LOGIN,
            audience=settings.AUTH0_AUDIENCE,
        )
    return RedirectResponse(url="/")


@router.get("/logout")
def logout(request: Request):
    response = RedirectResponse(
        url="https://"
        + settings.AUTH0_DOMAIN
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": request.url_for("home"),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        )
    )
    request.session.clear()
    return response


@router.route("/callback", methods=["GET", "POST"])
async def callback(request: Request):
    """
    Callback redirect from Auth0
    """
    token = await oauth.auth0.authorize_access_token(request)
    request.session["access_token"] = token["access_token"]
    request.session["id_token"] = token["id_token"]
    request.session["userinfo"] = token["userinfo"]
    return RedirectResponse(url=router.url_path_for("profile"))
