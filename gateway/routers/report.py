"""
APP Report for generating reports
"""
import requests
import settings
from fastapi import APIRouter, Security
from routers.blocking import VerifyToken

router = APIRouter()
auth = VerifyToken()


@router.get("/get-teacher-reports/list")
async def get_teacher_list(auth_result: str = Security(auth.verify)):
    api_url = f"http://{settings.FH_APP_REPORT_URL}/teacher-reports/list"
    teacher_report_list = requests.get(api_url).json()
    return teacher_report_list


@router.get("/get-teacher-report/{id}")
async def get_teacher_report(id: int, auth_result: str = Security(auth.verify)):
    api_url = f"http://{settings.FH_APP_REPORT_URL}/teacher-report/{id}"
    teacher_report = requests.get(api_url).json()
    return teacher_report
