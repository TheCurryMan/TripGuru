from bs4 import BeautifulSoup
import requests

def get_time(attraction, city):
    url = "https://www.tripadvisor.com/Attraction_Review-g60713-d105363-Reviews-Twin_Peaks-San_Francisco_California.html"
    r = requests.get(url)

    data = r.text

    soup = BeautifulSoup(data, "html.parser")

    samples = soup.find_all("div", class_="detail")
    narrow = samples[2].find_all("b")
    string = (str(samples[2]).replace(str(narrow[0]), ""))


    if "1" in string:
        return(1)
    if "2" in string:
        return(2)
    if "3" in string:
        return(3)
    if "4" in string:
        return(4)
    if "5" in string:
        return(5)
    if "6" in string:
        return(6)

