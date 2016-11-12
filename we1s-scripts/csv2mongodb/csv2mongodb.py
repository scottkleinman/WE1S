# -*- coding: UTF-8 -*-
# Config #
MONGO_URL = "mongodb://localhost:27017/"
DATABASE = "MyDB"
COLLECTION = "ribollita"
CSV = "C:/Users/Scott/Documents/washington_post-2007-h-master-clean.csv"

import pymongo, json, os, csv
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
#print client.database_names()
db = client["COLLECTION"]
#print db.collection_names()

'''
The following routine converts a CSV file to a list of JSON manifests 
and populates the ribollita collection with them. 
'''
# Convert CSV file to JSON
def csv2json(CSV):
    file = open(CSV)
    reader = csv.reader(file)
    data = list(reader)
    print(CSV)
    del data[0] # Remove the header row

    manifests = []    
    for row in data:
        # Get CSV column values as variables
        id = row[0]
        publication = row[1]
        pubDate = row[2]
        title = row[3]
        articleBody = row[4]
        author = row[5]
        docUrl = row[6]
        wordCount = row[7]

        # Write them to properties in the manifest
        manifest = {}
        manifest["_id"] = id
        manifest["namespace"] = "WE1Sv1.0"
        manifest["path"] = ",Corpus,Ribollita,RawData,"+id+","
        manifest["content"] = articleBody
        manifest["authors"] = [author]
        manifest["title"] = title
        manifest["label"] = id[:10]+"..." # First ten characters of title plus ellipsis
        manifest["description"] = "WE1S 'Ribollita' test corpus"
        manifest["group"] = {"editors": [ {"group": "WE1S"} ]}
        manifest["publication"] = publication
        manifest["pubDate"] = pubDate
        manifest["docUrl"] = docUrl
        manifest["wordCount"] = wordCount

        manifests.append(manifest)

    return manifests

# Insert a list of manifests into the database
def bulk_manifest_insert(manifests, COLLECTION):
    result = db[COLLECTION].insert_many(manifests)
    return "Success"

# For execution
manifests = csv2json(CSV)
result = bulk_manifest_insert(manifests, COLLECTION)
print result
#db[COLLECTION].delete_many({"namespace":"WE1Sv1.0"}) # Deletes everything for testing

'''
The function below uses a JSON object sent by Ajax to fetch the 
content of a single manifest and return it to the browser. 
'''
# Return the "content" value of a single record by _id from Ajax
def get_content(id, COLLECTION):
    #id = request.json["_id"] # For Ajax
    result = db[COLLECTION].find_one({"_id": id})
    return result["content"]

result = get_content("wp-2007-h-13", COLLECTION)
print result