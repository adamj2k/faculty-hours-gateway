"""
APP Faculty for handling Lectures, Subjects and hours for each subject
"""
import requests
import settings
from fastapi import APIRouter, Depends
from routers.blocking import ProtectedEndpoint

router = APIRouter()


@router.get("/get_subjects", dependencies=[Depends(ProtectedEndpoint)])
def get_subjects():
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty"
    all_subjects = requests.get(api_url).json()
    return {"subjects": all_subjects}
