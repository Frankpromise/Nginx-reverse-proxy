from flask import Flask
from elasticsearch import Elasticsearch

es = Elasticsearch(host='es')
app = Flask(__name__)

from . import routes