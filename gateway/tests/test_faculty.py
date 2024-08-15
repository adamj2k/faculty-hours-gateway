import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from gateway.routers.faculty import router, VerifyToken
from fastapi import Depends


app = FastAPI()
app.include_router(router, prefix="/faculty")

# Mock the VerifyToken dependency
def mock_verify_token():
    print("Mock verify token called")
    return {"sub": "mocked_user_id", "scope": "read:lectures"}

app.dependency_overrides[VerifyToken.verify] = mock_verify_token

@pytest.mark.asyncio
async def test_get_lecture():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        print("Sending request to /faculty/lecture/1")
        response = await ac.get("/faculty/lecture/1")
    print("Response status code:", response.status_code)
    print("Response JSON:", response.json())
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["id"] == 1
