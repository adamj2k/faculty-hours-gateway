"""
APP Report for generating reports
"""
from fastapi import APIRouter
from routers.blocking import VerifyToken

router = APIRouter()
auth = VerifyToken()
