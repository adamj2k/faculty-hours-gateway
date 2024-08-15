import base64
import datetime
import unittest
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from gateway.main import app
from gateway.routers.faculty import VerifyToken

mock_payload = {
    "http://127.0.0.1/roles": ["Standard User"],
    "iss": "https://dev-f5hlg1pvcd8s6oz7.eu.auth0.com/",
    "sub": "auth0|65fd3b8e196c760d876a6c6b",
    "aud": ["faculty-auth0-api", "https://dev-f5hlg1pvcd8s6oz7.eu.auth0.com/userinfo"],
    "iat": datetime.datetime.now(),
    "exp": datetime.datetime.now() + datetime.timedelta(minutes=30),
    "scope": "openid profile email",
    "azp": "LBoFiApH30YLUjvEPfBW3cJqJNoddIpG",
    "permissions": [],
}


header = base64.urlsafe_b64encode(b'{"alg":"RS256","typ":"JWT"}').decode("utf-8").rstrip("=")
payload = (
    base64.urlsafe_b64encode(b'{"sub":"1234567890","name":"John Doe","iat":1516239022}').decode("utf-8").rstrip("=")
)
signature = "dummy_signature"
test_token = f"{header}.{payload}.{signature}"


class TestGetTeacher(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = TestClient(self.app)
        self.payload = mock_payload
        self.mock_verify = MagicMock()
        self.mock_verify.verify.return_value = self.payload
        self.mock_verify.jwks_client.get_signing_key_from_jwt.return_value = MagicMock(key="dummy_signing_key")
        app.dependency_overrides[VerifyToken] = lambda: self.mock_verify

    @patch("requests.get")
    def test_get_teacher_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"name": "John", "last_name": "Doe", "id": 1}
        mock_get.return_value = mock_response

        response = self.client.get("faculty/teacher/1", headers={"Authorization": f"Bearer {test_token}"})
        print(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"name": "John", "last_name": "Doe", "id": 1})

    @patch("gateway.routers.faculty.VerifyToken.verify")
    def test_get_teacher_invalid_id(self, mock_verify):
        mock_verify.return_value = mock_payload
        response = self.client.get("faculty/teacher/abc")

        self.assertEqual(response.status_code, 422)

    @patch("requests.get")
    def test_get_teacher_non_existent_id(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"error": "Teacher not found"}
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        response = self.client.get("faculty/teacher/999")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"error": "Teacher not found"})

    @patch("gateway.routers.faculty.VerifyToken.verify")
    def test_get_teacher_auth_failure(self, mock_verify):
        mock_verify.side_effect = False

        response = self.client.get("faculty/teacher/1")

        self.assertEqual(response.status_code, 401)
