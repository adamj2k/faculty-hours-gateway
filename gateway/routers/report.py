"""
APP Report for generating reports
"""
import requests
from fastapi import APIRouter, Security

from gateway import settings
from gateway.routers.blocking import VerifyToken

router = APIRouter()
auth = VerifyToken()


@router.get("/teacher-reports/all")
async def get_teacher_list(auth_result: str = Security(auth.verify)):
    api_url = f"http://{settings.FH_APP_REPORT_URL}/teacher-reports/list"
    teacher_report_list = requests.get(api_url).json()
    return teacher_report_list


@router.get("/teacher-report/{id}")
async def get_teacher_report(id: int, auth_result: str = Security(auth.verify)):
    api_url = f"http://{settings.FH_APP_REPORT_URL}/teacher-report/{id}"
    teacher_report = requests.get(api_url).json()
    return teacher_report


@router.delete("/teacher-report/delete/{id}")
async def delete_teacher_report(id: int, auth_result: str = Security(auth.verify_with_admin)):
    api_url = f"http://{settings.FH_APP_REPORT_URL}/teacher-report/delete/{id}"
    teacher_report = requests.delete(api_url).json()
    return teacher_report


@router.get("/personal-workload-reports/all")
async def get_personal_workload_report(auth_result: str = Security(auth.verify)):
    api_url = f"http://{settings.FH_APP_REPORT_URL}/personal-workload-report/list"
    personal_workload_report = requests.get(api_url).json()
    return personal_workload_report


@router.get("/personal-workload-report/{id}")
async def get_personal_workload_report(id: int, auth_result: str = Security(auth.verify)):
    api_url = f"http://{settings.FH_APP_REPORT_URL}/personal-workload-report/{id}"
    personal_workload_report = requests.get(api_url).json()
    return personal_workload_report


@router.delete("/personal-workload-report/delete/{id}")
async def delete_personal_workload_report(id: int, auth_result: str = Security(auth.verify_with_admin)):
    api_url = f"http://{settings.FH_APP_REPORT_URL}/personal-workload-report/delete/{id}"
    personal_workload_report = requests.delete(api_url).json()
    return personal_workload_report


@router.get("summary-report/all")
async def get_summary_report(auth_result: str = Security(auth.verify)):
    api_url = f"http://{settings.FH_APP_REPORT_URL}/summary-report/all"
    summary_report = requests.get(api_url).json()
    return summary_report


@router.get("summary-report/{id}")
async def get_summary_report(id: int, auth_result: str = Security(auth.verify)):
    api_url = f"http://{settings.FH_APP_REPORT_URL}/summary-report/{id}"
    summary_report = requests.get(api_url).json()
    return summary_report


@router.delete("summary-report/delete/{id}")
async def delete_summary_report(id: int, auth_result: str = Security(auth.verify_with_admin)):
    api_url = f"http://{settings.FH_APP_REPORT_URL}/summary-report/delete/{id}"
    summary_report = requests.delete(api_url).json()
    return summary_report
