from flask import Flask, request
import json
from sort import sortAttractions

app = Flask(__name__)



@app.route('/', methods=['GET'])
def index():
  return "Hello this is cool"

@app.route('/attractions', methods=['GET', 'POST'])
def attractions():

  return getAttractions(request.args.get('city'))

@app.route('/sort', methods=['GET', 'POST'])
def sort():

  return sortAttractions(request.args.get('data'))


 

