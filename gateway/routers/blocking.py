from fastapi import HTTPException, Request, status


def ProtectedEndpoint(request: Request):
    if not "id_token" in request.session:
        raise HTTPException(
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
            detail="Not authorized",
            headers={"Location": "/login"},
        )
