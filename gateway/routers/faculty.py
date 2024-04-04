"""
APP Faculty for handling Lectures, Subjects and hours for each subject
"""
import requests
import settings
from fastapi import APIRouter, Depends, Security
from routers.blocking import ProtectedEndpoint, VerifyToken

router = APIRouter()
auth = VerifyToken()


@router.get("/get_subjects", dependencies=[Depends(ProtectedEndpoint)])
async def get_subjects(auth_result: str = Security(auth.verify)):
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty"
    all_subjects = requests.get(api_url).json()
    return {"subjects": all_subjects}
