import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from gateway.routers.faculty import router

app = FastAPI()
app.include_router(router, prefix="/faculty")

@pytest.mark.asyncio
async def test_get_lecture():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/faculty/lecture/1")
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["id"] == 1
