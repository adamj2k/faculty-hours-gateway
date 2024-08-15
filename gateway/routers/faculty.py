"""
APP Faculty for handling Lectures, Subjects and hours for each subject
"""
import requests
from fastapi import APIRouter, Security

from gateway import settings
from gateway.routers.blocking import VerifyToken

router = APIRouter()


@router.get("/teachers")
async def get_subjects(auth_result: str = Security(VerifyToken().verify)):
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty/teacher/list"
    all_teachers = requests.get(api_url).json()
    return all_teachers


@router.post("/create-teacher")
async def create_teacher(teacher: dict, auth_result: str = Security(VerifyToken().verify)):
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty/teacher/create"
    new_teacher = requests.post(api_url, json=teacher).json()
    return new_teacher


@router.get("/teacher/{id}")
async def get_teacher(id: int, auth_result: str = Security(VerifyToken().verify)):
    print(auth_result)
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty/teacher/{id}"
    teacher = requests.get(api_url).json()
    return teacher


@router.delete("/teacher/delete/{id}")
async def delete_teacher(id: int, auth_result: str = Security(VerifyToken().verify_with_admin)):
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty/teacher/delete/{id}"
    delete_teacher = requests.delete(api_url).json()
    return delete_teacher


@router.put("/teacher/update/{id}")
async def update_teacher(id: int, teacher: dict, auth_result: str = Security(VerifyToken().verify_with_admin)):
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty/teacher/update/{id}"
    update_teacher = requests.put(api_url, json=teacher).json()
    return update_teacher


@router.get("/lecture/{id}")
async def get_lecture(id: int, auth_result: str = Security(VerifyToken().verify)):
    print("Auth result in get_lecture:", auth_result)
    print("Auth result in get_lecture:", auth_result)
    print("Auth result in get_lecture:", auth_result)
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty/lecture/{id}"
    print("Requesting lecture from API:", api_url)
    lecture = requests.get(api_url).json()
    return lecture


@router.get("lecture/list")
async def get_lecture_list(auth_result: str = Security(VerifyToken().verify)):
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty/lecture/list"
    lecture_list = requests.get(api_url).json()
    return lecture_list


@router.post("lecture/create")
async def create_lecture(lecture: dict, auth_result: str = Security(VerifyToken().verify_with_admin)):
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty/lecture/create"
    new_lecture = requests.post(api_url, json=lecture).json()
    return new_lecture


@router.delete("lecture/delete/{id}")
async def delete_lecture(id: int, auth_result: str = Security(VerifyToken().verify_with_admin)):
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty/lecture/delete/{id}"
    delete_lecture = requests.delete(api_url).json()
    return delete_lecture


@router.get("exercise/{id}")
async def get_exercise(id: int, auth_result: str = Security(VerifyToken().verify)):
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty/exercise/{id}"
    exercise = requests.get(api_url).json()
    return exercise


@router.get("exercise/list")
async def get_exercise_list(auth_result: str = Security(VerifyToken().verify)):
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty/exercise/list"
    exercise_list = requests.get(api_url).json()
    return exercise_list


@router.post("exercise/create")
async def create_exercise(exercise: dict, auth_result: str = Security(VerifyToken().verify_with_admin)):
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty/exercise/create"
    new_exercise = requests.post(api_url, json=exercise).json()
    return new_exercise


@router.delete("exercise/delete/{id}")
async def delete_exercise(id: int, auth_result: str = Security(VerifyToken().verify_with_admin)):
    api_url = f"http://{settings.FH_APP_FACULTY_URL}/faculty/exercise/delete/{id}"
    delete_exercise = requests.delete(api_url).json()
    return delete_exercise
