from flask import Blueprint, request, Flask
from flask_restful import Resource, Api 

app = Flask(__name__)
api = Api(app)

class Hey(Resource):
    def get(self):
        return {'result': 'Hey'}

api.add_resource(Hey, '/')

if __name__ == '__main__':
    app.run(debug=True)
