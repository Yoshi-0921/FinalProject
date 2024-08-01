import os

dir_path = os.path.dirname(os.path.realpath(__file__))
CATEGORIES = open(os.path.join(dir_path, "categories.json"), "r").read().splitlines()
