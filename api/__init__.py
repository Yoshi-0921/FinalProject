from config import API
from main import app

api = API(app)


# ENDPOINTS
# -------------- USER  ---------------
from .user import *

api.add_resource(User, User.API_PREFIX)

# -------------- OPENAI ---------------
from chat import *

api.add_resource(OpenAI, OpenAI.API_PREFIX)

# -------------- STOCK ---------------
from .stock import *

api.add_resource(Stock, Stock.API_PREFIX)
