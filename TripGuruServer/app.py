from flask import Flask, request
import json
from getAttractionsFromName import getAttractions
from getReviews import get_revs, calculate_review_num
from sort import sortAttractions
from getWeather import get_hourly_weather

app = Flask(__name__)



@app.route('/', methods=['GET'])
def index():
  return "Hello this is cool"

@app.route('/attractions', methods=['GET', 'POST'])
def attractions():

  return getAttractions(request.args.get('city'))

@app.route('/sort', methods=['GET', 'POST'])
def sort():
  print( sortAttractions(request.args.get('data')))



 

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():

  allReviews = get_revs(request.args.get('attraction'), request.args.get('city'))
  print(allReviews)
  finalStr = ""
  scoreText = calculate_review_num(allReviews)
  for rev in allReviews:
    finalStr = finalStr + rev + "|"
  return finalStr + str(scoreText)


