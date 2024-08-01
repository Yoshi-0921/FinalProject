from config import API
from main import app

api = API(app)


# ENDPOINTS
# -------------- USER  ---------------
from .user import *

api.add_resource(User, *User.END_POINTS)
api.add_resource(UserPositions, *UserPositions.END_POINTS)

# -------------- OPENAI ---------------
from chat import *

api.add_resource(OpenAI, *OpenAI.END_POINTS)

# -------------- STOCK ---------------
from .stock import *

api.add_resource(Stock, *Stock.END_POINTS)
