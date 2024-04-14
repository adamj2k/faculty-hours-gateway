from typing import Optional

import jwt
import settings
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes


class UnauthorizedException(HTTPException):
    def __init__(self, detail: str, **kwargs):
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)


class UnauthenticatedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Requires authentication")


def ProtectedEndpoint(request: Request):
    if not "id_token" in request.session:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail="Not authorized",
            headers={"Location": "/login"},
        )


class VerifyToken:
    def __init__(self) -> None:
        jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    async def verify(
        self,
        security_scopes: SecurityScopes,
        token: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer()),
    ):
        if token is None:
            raise UnauthenticatedException

        try:
            signing_key = self.jwks_client.get_signing_key_from_jwt(token.credentials).key
        except jwt.exceptions.PyJWKClientError as error:
            raise UnauthorizedException(str(error))
        except jwt.exceptions.DecodeError as error:
            raise UnauthorizedException(str(error))

        try:
            payload = jwt.decode(
                token.credentials,
                signing_key,
                algorithms=settings.AUTH0_ALGORITHMS,
                audience=settings.AUTH0_AUDIENCE,
                issuer=settings.AUTH0_ISSUER,
            )
        except Exception as error:
            raise UnauthorizedException(str(error))

        return payload
