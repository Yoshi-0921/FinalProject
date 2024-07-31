from flask import Blueprint, request, Flask
from flask_restful import Resource, Api 
from api import app

if __name__ == '__main__':
    print("Launching app")
    app.run(debug=True)
