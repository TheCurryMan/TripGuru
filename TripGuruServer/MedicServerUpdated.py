from flask import Flask, request, render_template
import twilio.twiml
from twilio.rest import TwilioRestClient
from getMessage import getMessage
from locationBasedAnalysis import getCoordinates
import json

"""
Overall flask app
"""

app = Flask(__name__)
# Try adding your own number to this list!
account_sid = "ACa9eca256e7d2b82539a0c6086dc244d7"
auth_token = "213a8dd83633246a86c5b36361665220"
client = TwilioRestClient(account_sid, auth_token)

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():

    #Getting actual message from user
    body = request.values.get('Body', None)

    #Getting any image the user might have sent
    img_url = request.values.get('MediaUrl0', None)

    #Getting the from number from the user
    from_number = request.values.get('From', None)

    #Gets the message that's returned back to the user
    message = getMessage(from_number, body, img_url)

    #Sends the message back
    resp = twilio.twiml.Response()
    resp.message(message)
    return str(resp)


@app.route('/map')
def map():

    coords = getCoordinates()

    print(coords)

    india = [[22.727960, 75.883014, 'Common cold'], [22.728616, 75.875674, 'Common cold'], [22.717346, 75.863291, 'Common cold'], [22.724524, 75.849694, 'Chicken Pox'], [22.716895, 75.842695, 'Common cold'], [22.710365, 75.851142, 'Common cold'], [22.729639, 75.843573
,'Common cold'], [22.716730, 75.836905, 'Common cold'], [22.701517, 75.865168, 'Influenza'], [22.723220, 75.860087, 'Chicken Pox']]

    coords = [[37.2871722990697, -122.009842650786, 'Influenza'], [37.3101947831752, -122.004153167078, 'Influenza'], [37.3298288045343, -121.910716096225, 'Influenza'], [37.31594885, -122.01996163725, 'Influenza'], [37.3100288449176, -122.003983462297, 'Influenza'], [37.3099979297936, -122.003994515512, 'Influenza'], [37.3100288449176, -122.003983462297, 'Influenza'], [37.2979177586207, -121.987272689655, 'Influenza'], [37.3220811926897, -121.988135347461, 'Influenza'], [37.3100288449176, -122.003983462297, 'Influenza'], [37.3100288449176, -122.003983462297, 'Adverse drug reaction'], [37.29659505, -122.036754042628, 'Chicken Pox'], [37.3118038, -122.03560287258, 'Chicken Pox'], [37.32868365, -122.039170157567, 'Chicken Pox'], [37.32464415, -122.055316050365, 'Chicken Pox'], [37.30812525, -122.051758406113, 'Chicken Pox'], [37.3100288449176, -122.003983462297, 'Chicken Pox'], [37.3472192, -122.057645195855, 'Chicken Pox'], [37.3100288449176, -122.003983462297, 'Anxiety disorder'], [37.3100288449176, -122.003983462297, 'Major depressive disorder'], [37.3096983265306, -122.006097285714, 'Allergy'], [37.3100288449176, -122.003983462297, 'Allergy'], [36.567459, -121.9158229, 'Nasopharyngitis'], [39.677265360654, -75.0345911046285, 'Common cold'], [37.3100288449176, -122.003983462297, 'Common cold'], [37.3100288449176, -122.003983462297, 'Gastroesophageal reflux disease']]
    coords += india

    return render_template('index.html', data=coords)


if __name__ == "__main__":
    app.run(debug=True)