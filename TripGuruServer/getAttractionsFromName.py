from yelpapi import YelpAPI
import collections
import json
from getImage import getImageURLfromName
# import json
# import pprint
#from firebase import firebase


def getAttractions(name):
    #firebase = firebase.FirebaseApplication('https://tripguru-a156e.firebaseio.com/', None)
    #city_tree = firebase.get("/Cities", None)


    client_id = "MRWYCFCN23JZYHMqUG20CA"
    client_secret = "vcy71k5kcNFtQJ4u6WnvyqmvtfsstSBawSMfQV5HhGdBDNu0iVVCZWtGcLpmg1QJ"

    def convert(data):
        if isinstance(data, basestring):
            return str(data)
        elif isinstance(data, collections.Mapping):
            return dict(map(convert, data.iteritems()))
        elif isinstance(data, collections.Iterable):
            return type(data)(map(convert, data))
        else:
            return data

    yelp_api = YelpAPI(client_id, client_secret)
    search_results = yelp_api.search_query(term='attraction', location=name, sort_by='rating', limit=5)
    converted = (convert(search_results))

    val = "Attraction"
    counter = 1
    finalDict = {}
    for places in converted["businesses"]:
        idx = val + str(counter)
        name = places["name"]
        lat = places['coordinates']['latitude']
        lng = places['coordinates']['longitude']
        url = getImageURLfromName(name)
        finalDict[name] = {"lat": lat, "long":lng, "url":url}


        #firebase.put('', '/Cities/San Francisco/' + idx + '/name', name)
        #firebase.put('', '/Cities/San Francisco/' + idx + '/lat', lat)
        #firebase.put('', '/Cities/San Francisco/' + idx + '/lng', lng)
        #counter = counter + 1
    return json.dumps(finalDict)