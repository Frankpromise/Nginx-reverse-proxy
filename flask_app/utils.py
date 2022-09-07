import sys
import time
import requests
from elasticsearch import exceptions
from flask_app import es


def load_data_in_es():
    """ creates an index in elasticsearch """
    url = "http://data.sfgov.org/resource/rqzj-sfat.json"
    r = requests.get(url)
    data = r.json()
    print "Loading data in elasticsearch ..."
    for id, truck in enumerate(data):
        res = es.index(index="sfdata", doc_type="truck", id=id, body=truck)
    print "Total trucks loaded: ", len(data)

def safe_check_index(index, retry=3):
    """ connect to ES with retry """
    if not retry:
        print "Out of retries. Bailing out..."
        sys.exit(1)
    try:
        status = es.indices.exists(index)
        return status
    except exceptions.ConnectionError as e:
        print "Unable to connect to ES. Retrying in 5 secs..."
        time.sleep(5)
        safe_check_index(index, retry-1)

def format_fooditems(string):
    items = [x.strip().lower() for x in string.split(":")]
    return items[1:] if items[0].find("cold truck") > -1 else items

def check_and_load_index():
    """ checks if index exits and loads the data accordingly """
    if not safe_check_index('sfdata'):
        print "Index not found..."
        load_data_in_es()
