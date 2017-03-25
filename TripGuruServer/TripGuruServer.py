from flask import Flask

"""
Overall flask app
"""

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello_monkey():

    return("Does this work? ")


if __name__ == "__main__":
    app.run(debug=True)