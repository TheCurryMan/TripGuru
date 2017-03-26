import requests
import ast
API_key = "1763e5ce6e054083800110513172603"

twelve_hour = ""

def get_hourly_weather(city, state):
    url = "https://api.apixu.com/v1/forecast.json?key=" + API_key + "&q=" + city
    r = requests.get(url)
    res = r.text
    rev = ast.literal_eval(res)
    for item in rev['forecast']['forecastday'][0]['hour']:
        twelve_hour = twelve_hour + item['will_it_rain'] + ","
    return twelve_hour[:-1]
