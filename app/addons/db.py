import pymongo
import datetime
from app.addons.dt import to_log

# DB
####
def dbSend(mongo_host, mongo_port, mongo_database, uuidResp, projectIp, headers):
    client = pymongo.MongoClient(mongo_host, mongo_port)
    db = client[mongo_database]
    if uuidResp in db.list_collection_names():
        collection = db[uuidResp]
    else:
        collection = db.create_collection(uuidResp)
  
    data = to_log( url =     projectIp + '/api/v1/metrics/project/' + str(uuidResp) + '/current',
                   headers = headers )
    data["time"] = str(datetime.datetime.now()).split('.')[0]

    collection.insert_one(data)
    client.close()

def dbGet(mongo_host, mongo_port, mongo_database):
    client = pymongo.MongoClient(mongo_host, mongo_port)
    db = client[mongo_database]
    for collection_name in db.list_collection_names():
        print("project: " + collection_name)
        collection_t = db[collection_name]
        cursor = collection_t.find({})
        for document in cursor:
            print(document)

    client.close()