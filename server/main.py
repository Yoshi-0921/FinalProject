from flask import Flask


app = Flask(__name__)

from api import *

if __name__ == '__main__':
    print("Launching app")
    app.run(debug=True)
