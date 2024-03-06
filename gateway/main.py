import settings
import uvicorn
from fastapi import FastAPI
from fastapi.security import HTTPBearer
from routers import auth
from starlette.middleware.sessions import SessionMiddleware

token_auth_scheme = HTTPBearer()

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=settings.AUTH0_SESSION_SECRET)

app.include_router(auth.router, prefix="")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
