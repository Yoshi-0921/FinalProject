import os
from datetime import datetime

from dotenv import load_dotenv
from flask_restful import Api, Resource
from flask_restx import Api as ApiX
from flask_restx import Resource as ResourceX

load_dotenv()


OPENAI_KEY = os.getenv('OPENAI_KEY')
DEBUG = os.getenv('DEBUG')

RESOUCE = ResourceX if DEBUG else Resource
API = ApiX if DEBUG else Api

SQLITE_PATH = "server/static/market/market.sqlite"

TODAY = datetime(2024, 7, 31, 9, 0, 0)
