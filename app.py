# Import Flask dependency 
from flask import Flask

# Create a new Flask app 
app = Flask(__name__)

# Create flask routes
@app.route('/')
def hello_world():
    return 'Hello world'

