from bs4 import BeautifulSoup
import requests
import ast

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
        r = requests.post("http://text-processing.com/api/sentiment/", data={'text': item})
        revs = r.text
        rev = ast.literal_eval(revs)
        label = rev['label']
        perc = rev['probability'][label]
        sum = (sum + perc)
    return sum/len(reviews) * 10
