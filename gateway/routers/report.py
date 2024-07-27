"""
APP Report for generating reports
"""
import requests
import settings
from fastapi import APIRouter, Security
from routers.blocking import VerifyToken

router = APIRouter()
auth = VerifyToken()


@router.get("/teacher-reports/list")
async def get_subjects(auth_result: str = Security(auth.verify)):
    api_url = f"http://{settings.FH_APP_REPORT_URL}/teacher-reports/list"
    teacher_report_list = requests.get(api_url).json()
    return teacher_report_list
