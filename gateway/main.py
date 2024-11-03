import strawberry
import strawberry.fastapi
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from starlette.middleware.sessions import SessionMiddleware

from gateway import settings
from gateway.routers.auth import router as auth_router
from gateway.routers.faculty import router as faculty_router
from gateway.routers.payrolls import MonthPayrollsQuery
from gateway.routers.report import router as report_router

token_auth_scheme = HTTPBearer()
schema = strawberry.Schema(query=MonthPayrollsQuery)
graphql_app = strawberry.fastapi.GraphQLRouter(
    schema, graphiql=True, allow_queries_via_get=True, context_getter=lambda: {"request": None}
)
app = FastAPI()

origins = [
    "http://localhost:8100",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8100",
    "http://localhost:8200",
    "http://127.0.0.1:8200",
    "http://localhost:8300",
    "http://127.0.0.1:8300",
    "http://localhost:8400",
    "http://127.0.0.1:8400",
]

app.add_middleware(SessionMiddleware, secret_key=settings.AUTH0_SESSION_SECRET)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


app.include_router(auth_router, prefix="")
app.include_router(faculty_router, prefix="/faculty")
app.include_router(report_router, prefix="/report")
app.include_router(graphql_app, prefix="/payrolls")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
