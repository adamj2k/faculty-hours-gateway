"""
APP Faculty for handling Lectures, Subjects and hours for each subject
"""
import requests
import settings
from fastapi import APIRouter, Security
from routers.blocking import VerifyToken

router = APIRouter()
auth = VerifyToken()


@router.get("/get-teachers")
async def get_subjects(auth_result: str = Security(auth.verify)):
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty/teachers/list"
    all_teachers = requests.get(api_url).json()
    return all_teachers


@router.post("/create-teacher")
async def create_teacher(teacher: dict, auth_result: str = Security(auth.verify)):
    auth.check_role(auth_result, "Administrator")
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty/teacher/create"
    new_teacher = requests.post(api_url, json=teacher).json()
    return new_teacher


@router.get("/get_teacher/{id}")
async def get_teacher(id: int, auth_result: str = Security(auth.verify)):
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty/teacher/{id}"
    teacher = requests.get(api_url).json()
    return teacher
