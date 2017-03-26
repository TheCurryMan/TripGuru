from bs4 import BeautifulSoup
import requests
import ast
from textblob import TextBlob
from math import ceil

def get_revs(attraction, city):
    print(attraction)
    print(city)
    attraction = convertSpaces(attraction)
    city = convertSpaces(city)
    url = "https://www.yelp.com/biz/" + attraction + "-" + city
    r = requests.get(url)

    data = r.text
    soup = BeautifulSoup(data, "html.parser")

    reviews = []
    for item in soup.findAll("p", {"class": "quote"}):
        reviews.append(item.text[13:-15].encode('ascii', errors='ignore'))
    return reviews

def convertSpaces(name):
    return (name.replace(" ", "-" ))

def calculate_review_num(reviews):
    sum = 0
    for item in reviews:
        blob = TextBlob(item)
        sum = sum + (blob.sentiment.polarity)
        final = ceil(sum * 100.0) /100.0
    return "The sentiment analysis for the reviews is : " + str(final/len(reviews) * 10) + "/10.0"

print(get_revs("Japanese Tea Garden",  "San Francisco"))