"""
APP Faculty for handling Lectures, Subjects and hours for each subject
"""
import requests
from fastapi import APIRouter, Depends
from routers.blocking import ProtectedEndpoint

router = APIRouter()


@router.get("/get_subjects", dependencies=[Depends(ProtectedEndpoint)])
def get_subjects():
    api_url = "http://127.0.0.1:8100/faculty"
    all_subjects = requests.get(api_url).json()
    return {"subjects": all_subjects}
