from main import api
from chat import *

api.add_resource(OpenAI, OpenAI.USER_API_PREFIX) # /users

