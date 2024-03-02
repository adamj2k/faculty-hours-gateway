import uvicorn
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from starlette.middleware.sessions import SessionMiddleware

import settings
from API.routers import auth

token_auth_scheme = HTTPBearer()

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=settings.AUTH0_SESSION_SECRET)

app.include_router(auth.router, prefix="")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
