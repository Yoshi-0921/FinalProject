import os
from datetime import datetime

from dotenv import load_dotenv
from flask_restful import Api, Resource
from flask_restx import Api as ApiX
from flask_restx import Resource as ResourceX

load_dotenv()


OPENAI_KEY = os.getenv("OPENAI_KEY")
DEBUG = os.getenv("DEBUG")

RESOUCE = ResourceX if DEBUG else Resource
API = ApiX if DEBUG else Api

<<<<<<< HEAD
SQLITE_PATH = "server/static/market/market.sqlite"
=======

SQLITE_FILE_NAME = "market.sqlite"
current_script_dir = os.path.dirname(os.path.abspath(__file__))
relative_path = os.path.join("..", "static", "market", SQLITE_FILE_NAME)
SQLITE_PATH = os.path.abspath(os.path.join(current_script_dir, relative_path))
>>>>>>> 4d88f3c (merge)

TODAY = datetime(2024, 7, 31, 9, 0, 0)
