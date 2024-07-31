import os
from dotenv import load_dotenv
from flask_restful import Resource, Api
from flask_restx import Resource as ResourceX, Api as ApiX


load_dotenv()


OPENAI_KEY = os.getenv('OPENAI_KEY')
DEBUG = os.getenv('DEBUG')

RESOUCE = ResourceX if DEBUG else Resource
API = ApiX if DEBUG else Api