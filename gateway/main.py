import settings
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from routers import auth, faculty
from starlette.middleware.sessions import SessionMiddleware

token_auth_scheme = HTTPBearer()

app = FastAPI()

origins = [
    "http://localhost:8100",
    "http://localhost:8000",
]

app.add_middleware(SessionMiddleware, secret_key=settings.AUTH0_SESSION_SECRET)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="")
app.include_router(faculty.router, prefix="/faculty")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
