from yelpapi import YelpAPI
import collections
import json
import pprint
from  firebase import firebase

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
search_results = yelp_api.search_query(term='tourist attraction', location='san francisco, ca', sort_by='rating', limit=5)
converted = (convert(search_results))

for places in converted["businesses"]:
    print(places["name"])

def getLat(data):

def getLng(data):



