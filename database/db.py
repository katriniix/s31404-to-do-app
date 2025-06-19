from flask.cli import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri, tls = True)
db = client.get_database("calendar")