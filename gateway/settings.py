import os

from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
AUTH0_AUDIENCE = os.getenv("AUTH0_AUDIENCE")
AUTH0_SESSION_SECRET = os.getenv("SECRET_KEY")
AUTH0_LOGIN = os.getenv("AUTH0_LOGIN")
HOST = os.getenv("HOST")
FH_APP_FACULTY_URL = os.getenv("FH_APP_FACULTY_URL")
