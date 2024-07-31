import os

from dotenv import load_dotenv
from flask_restful import Api, Resource
from flask_restx import Api as ApiX
from flask_restx import Resource as ResourceX

load_dotenv()


OPENAI_KEY = os.getenv('OPENAI_KEY')
DEBUG = os.getenv('DEBUG')

RESOUCE = ResourceX if DEBUG else Resource
API = ApiX if DEBUG else Api

SQLITE_PATH = "static/market/market.sqlite"
