from flask import Blueprint, request, Flask
from flask_restful import Resource, Api 



class User(Resource):
    USER_API_PREFIX = 'users'
    def get(self):
        return {'users': ['Weimeng']}

