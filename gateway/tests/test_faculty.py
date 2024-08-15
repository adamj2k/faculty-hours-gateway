import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI
from gateway.routers.faculty import router, VerifyToken
from fastapi import Security
from fastapi.security import HTTPBearer


app = FastAPI()
app.include_router(router, prefix="/faculty")

# Mock the VerifyToken dependency
def mock_verify_token(security_scopes, token=Security(HTTPBearer())):
    print("Mock verify token called with scopes:", security_scopes.scopes, "and token:", token)
    result = {"sub": "mocked_user_id", "scope": "read:lectures"}
    print("Mock verify token result:", result)
    return result

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
