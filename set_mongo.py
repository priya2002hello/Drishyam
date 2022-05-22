import pymongo
import os
from dotenv import load_dotenv,find_dotenv

load_dotenv(find_dotenv())
mongoURl=os.getenv('MongoURI')
try:
    client = pymongo.MongoClient(mongoURl)

    print(client.server_info())
    dbname = client["Records"]

    criminal_records = dbname["criminal_records"]
    candidate_records=dbname["candidate_records"]
except Exception:
    print("MongoDb connection not successful")