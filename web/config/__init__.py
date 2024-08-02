import os

from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv('NEWS_API_KEY')

dir_path = os.path.dirname(os.path.realpath(__file__))
# CATEGORIES = open(os.path.join(dir_path, "categories.json"), "r").read().splitlines()
