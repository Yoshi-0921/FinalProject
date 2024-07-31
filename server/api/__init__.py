from config import API
from main import app

api = API(app)


# ------------------------------- USER ENDPOINTS --------------------------------
from .user import *

api.add_resource(User, User.USER_API_PREFIX) # /users

# ------------------------------- OPENAI ENDPOINTS --------------------------------
from chat import *

api.add_resource(OpenAI, OpenAI.OPENAI_API_PREFIX) # /openai

from .stock import *

api.add_resource(Stock, Stock.STOCK_API_PREFIX)
