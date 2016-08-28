import json
import os
import re

from flask import Flask, render_template
from flask import request
from pymongo import MongoClient

app = Flask(__name__)
## Supply IP address and port number
db_config = os.getenv('MONGO_URL', 'mongodb://dbuser:we1s@ds023435.mlab.com:23435/we1s')


### Index Route ###
@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")


### Eventually This Will Contain an Upload Function ###
@app.route("/upload-test", methods=["GET", "POST"])
def uploadTest():
    return render_template("upload-test.html")


### Eventually This Will Contain an Upload Function ###
@app.route("/upload-test/process", methods=["GET", "POST"])
def uploadTestProcess():
    # if request.method == 'POST':
    # file = request.files['file']
    print("Files: ")
    print(file)
    s = {"files": [
        {
            "name": "picture1.jpg",
            "size": 902604,
            "url": "http:\/\/example.org\/files\/picture1.jpg",
            "thumbnailUrl": "http:\/\/example.org\/files\/thumbnail\/picture1.jpg",
            "deleteUrl": "http:\/\/example.org\/files\/picture1.jpg",
            "deleteType": "DELETE"
        },
        {
            "name": "picture2.jpg",
            "size": 841946,
            "url": "http:\/\/example.org\/files\/picture2.jpg",
            "thumbnailUrl": "http:\/\/example.org\/files\/thumbnail\/picture2.jpg",
            "deleteUrl": "http:\/\/example.org\/files\/picture2.jpg",
            "deleteType": "DELETE"
        }
    ]}
    s = json.dumps(s)
    return s


### Eventually This Will Contain an Upload Function ###
@app.route("/upload", methods=["GET", "POST"])
def upload():
    return render_template("upload.html")


### Eventually This Will Contain an Upload Handler Function ###
@app.route("/upload/handler", methods=["POST"])
def uploadHandler():
    form = request.form
    headers = request.data
    print("Data:")
    print(headers)
    moo = json.dumps('success')
    print(moo)
    for key, value in form.items():
        print key, "=>", value
    return moo


### Search Function ###
@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Searches the whole database
    """
    # response = request.json['search']
    jsonObj = request.get_json()
    query = str(jsonObj['query'])
    regex = re.compile(query, re.IGNORECASE)
    results = []
    # Build a pymongo command to search the document by query term. Only executes if active is set to True.
    # Only matches _id
    active = True
    client = MongoClient(db_config)
    if active == True:
        # Search Publications
        db = client['Publications']
        publications = db['Publications']
        pcount = publications.find({"_id": regex}).count()
        p = publications.find({"_id": regex})
        # Search Corpus
        db = client['Corpus']
        corpus = db['Corpus']
        ccount = corpus.find({"_id": regex}).count()
        c = corpus.find({"_id": regex})

        htmlResult = ""
        if pcount == 0:
            htmlResult = "<h4>No publications found.</h4>"
        else:
            htmlResult = "<h4>Publications: " + str(pcount) + "</h4>"
            htmlResult += "<ul>"
            for item in p:
                args = '?_id=' + item["_id"] + '&amp;path=' + item["path"]
                htmlResult += '<li><a href="/publications/edit' + args + '">' + item["_id"] + '</a></li>'
            htmlResult += "</ul>"

        htmlResult += "<hr>"

        if ccount == 0:
            htmlResult += "<h4>No corpus items found.</h4>"
        else:
            htmlResult += "<h4>Corpus: " + str(ccount) + "</h4>"
            htmlResult += "<ul>"
            for item in c:
                args = '?_id=' + item["_id"] + '&amp;path=' + item["path"]
                htmlResult += '<li><a href="/corpus/collection/edit' + args + '">' + item["_id"] + '</a></li>'
            htmlResult += "</ul>"

    # Return the Ajax response
    return htmlResult


#########################
### Display Functions ###
#########################
@app.route("/display/publications", methods=["GET", "POST"])
def displayPublications():
    """
    Page to query all publications records. Sends a list of publications.
    NB. Date ranges are displayed as dict objects since there's no point 
    in parsing them out for a temporary html list. That can be done once 
    a final display layout is designed.
    """
    active = True
    result = ""
    if active == True:
        client = MongoClient(db_config)
        db = client['Publications']
        publications = db['Publications']
        result = publications.find()
        results = []
        for publication in result:
            results.append(publication)
    return render_template("displayPublications.html", results=results)


@app.route("/display/corpus", methods=["GET", "POST"])
def displayCorpus():
    """
    Page to query all corpus records. Sends a list of collections.
    NB. Date ranges are displayed as dict objects since there's no point 
    in parsing them out for a temporary html list. That can be done once 
    a final display layout is designed.
    """
    active = True
    result = ""
    if active == True:
        client = MongoClient(db_config)
        db = client['Corpus']
        corpus = db['Corpus']
        result = corpus.find()
        results = []
        for collection in result:
            results.append(collection)
    return render_template("displayCorpus.html", results=results)


#####################
### Add Functions ###
#####################
@app.route("/publications/add", methods=["GET", "POST"])
def addPublication():
    """
    Form for creating publications manifests. Form data gets submitted by Ajax.
    """
    preloaded = [
        {"description": "bortaS <b>bIr</b> jablu'DI' reH QaQqu' nay'!"},
        {"language": "en"},
        {"country": "usa"}
    ]
    return render_template("addPublication.html", msg="", preloaded=preloaded)


@app.route("/corpus/add", methods=["GET", "POST"])
def addCollection():
    """
    Form for creating collection manifests. Form data gets submitted by Ajax.
    """
    return render_template("addCollection.html")


@app.route("/corpus/collection/add", methods=["GET", "POST"])
def addCollectionNode():
    """
    Form for creating collection manifests. Form data gets submitted by Ajax.
    """
    return render_template("addCollectionNode.html")


@app.route("/corpus/raw-data/add", methods=["GET", "POST"])
def addRawDataNode():
    """
    Form for creating RawData manifests. Form data gets submitted by Ajax.
    """
    return render_template("addRawDataNode.html")


@app.route("/corpus/processed-data/add", methods=["GET", "POST"])
def addProcessedDataNode():
    """
    Form for creating processedData manifests. Form data gets submitted by Ajax.
    """
    return render_template("addProcessedDataNode.html")


@app.route("/corpus/metadata/add", methods=["GET", "POST"])
def addMetadataNode():
    """
    Form for creating metadata manifests. Form data gets submitted by Ajax.
    """
    return render_template("addMetadataNode.html")


@app.route("/corpus/outputs/add", methods=["GET", "POST"])
def addOutputsNode():
    """
    Form for creating outputs manifests. Form data gets submitted by Ajax.
    """
    return render_template("addOutputsNode.html")


@app.route("/corpus/related/add", methods=["GET", "POST"])
def addRelatedNode():
    """
    Form for creating related manifests. Form data gets submitted by Ajax.
    """
    return render_template("addRelatedNode.html")


@app.route("/corpus/generic/add", methods=["GET", "POST"])
def addGenericNode():
    """
    Form for creating generic manifests. Form data gets submitted by Ajax.
    """
    return render_template("addGenericNode.html")


######################
### Edit Functions ###
######################
@app.route("/publications/edit", methods=["GET", "POST"])
def editPublication():
    """
    Form for editing a pre-existing record.
    """
    # Get _id and path from url
    id = request.args.get("_id")
    path = request.args.get("path")

    # Execute database query
    active = True
    result = ""
    if active == True:
        client = MongoClient(db_config)
        db = client['Publications']
        publications = db['Publications']
    result = publications.find_one({"_id": id, "path": path})

    # Pre-processing
    del result["htmlResult"]  # Remove HTML output
    result["path"].replace(",", "/")  # Place slashes in path

    # Handle dates
    if len(result["date"]) == 10:
        date = result["date"]
        result["date"] = {"toggledaterange": False, "sdate": date, "start": date, "end": date}
    else:
        # Format: {'start': '2014-01-01', 'end': '2015-10-01'}
        print("Result Date")
        date = str(result["date"][0]).replace("'", "\"")
        dates = json.loads(date)
        start = dates["start"]
        end = dates["end"]
        result["date"] = {"toggledaterange": True, "sdate": start, "start": start, "end": end}

    # Convert to json stringØ
    jsonStr = json.dumps(result)

    return render_template("editPublication.html", results=jsonStr)


@app.route("/corpus/collection/edit", methods=["GET", "POST"])
def editCollectionNode():
    """
    Form for creating collection manifests. Form data gets submitted by Ajax.
    """
    """
    Form for editing a pre-existing record.
    """
    # Get _id and path from url
    id = request.args.get("_id")
    path = request.args.get("path")

    # Execute database query
    active = True
    result = ""
    if active == True:
        client = MongoClient(db_config)
        db = client['Corpus']
        corpus = db['Corpus']
    result = corpus.find_one({"_id": id, "path": path})

    # Pre-processing
    del result["htmlResult"]  # Remove HTML output
    result["path"].replace(",", "/")  # Place slashes in path

    # Handle dates
    if len(result["date"]) == 10:
        date = result["date"]
        result["date"] = {"toggledaterange": False, "sdate": date, "start": date, "end": date}
    else:
        # Format: {'start': '2014-01-01', 'end': '2015-10-01'}
        print("Result Date")
        date = str(result["date"][0]).replace("'", "\"")
        dates = json.loads(date)
        start = dates["start"]
        end = dates["end"]
        result["date"] = {"toggledaterange": True, "sdate": start, "start": start, "end": end}

    # Convert to json string
    jsonStr = json.dumps(result)

    return render_template("editCollectionNode.html", results=jsonStr)


#####################################
### Add/Edit Processing Functions ###
#####################################
@app.route("/process", methods=["GET", "POST"])
def process():
    """
    Gets the submitted json string, trims whitespace from the values, and returns the 
    json string along with an html string listing the values saved to the database.
    """
    jsonObj = request.get_json()

    # Start by pulling out the date toggle state
    for key, value in jsonObj.iteritems():
        if isinstance(value, dict):
            for k in value.keys():
                if k == "toggledaterange":
                    datetoggle = value[k]
                    del jsonObj[key][k]

    # Next modify the date
    if datetoggle == False:
        jsonObj["date"] = jsonObj["date"]["sdate"]
    else:
        l = []
        start = jsonObj["date"]["start"].encode('unicode-escape')
        end = jsonObj["date"]["end"].encode('unicode-escape')
        l.append(str({"start": start, "end": end}))
        jsonObj["date"] = l

    # Start an html list
    htmlResult = "<ul>"
    # Trim whitespace from the values of the json object
    for key, value in jsonObj.iteritems():
        # The value is a string
        if isinstance(value, basestring):
            stripped = value.strip(' \t\n\r')
            htmlResult += "<li><b>" + key + "</b>: " + stripped + "</li>"
        # The value is a list
        else:
            stripped = []
            htmlResult += "<li><b>" + key + "</b>:<ul>"
            for item in value:
                item = item.strip(' \t\n\r')
                stripped.append(item)
                htmlResult += "<li>" + item + "</li>"
            htmlResult += "</ul></li>"
        jsonObj[key] = stripped
    htmlResult += "</ul>"
    # The html has to be packaged in the json object for Flask to return it in the response.
    # Move the rest of the json for the database to another variable.
    jsonForDB = jsonObj
    htmlResult = {"htmlResult": htmlResult}
    jsonObj.update(htmlResult)
    jsonResult = json.dumps(jsonObj, sort_keys=False, indent=4, separators=(',', ': '))

    # Change slashes to commas in the path
    jsonForDB["path"] = jsonForDB["path"].replace("/", ",")
    jsonForDB = json.dumps(jsonForDB, sort_keys=False, indent=4, separators=(',', ': '))

    # Build a pymongo command to insert the data in the database. This should probably be moved 
    # to a separate function. Database data will not be saved unless active is set to True.
    active = True
    if active == True:
        client = MongoClient(db_config)
        db = client['Publications']
        publications = db['Publications']
        # Straightforward insert -- publications.insert(jsonForDB)
        # Upsert is better because it works for add and edit
        id = jsonForDB.pop("_id")
        publications.update({"_id": id}, {"$set": jsonForDB}, upsert=True)

    # Return the Ajax response
    return jsonResult


@app.route("/process/collection", methods=["POST"])
def processCollectionNode():
    """
    Gets the submitted json string, trims whitespace from the values, and returns the 
    json string along with an html string listing the values saved to the database.
    """
    jsonObj = request.get_json()

    # Start by pulling out the date toggle state
    for key, value in jsonObj.iteritems():
        if isinstance(value, dict):
            for k in value.keys():
                if k == "toggledaterange":
                    datetoggle = value[k]
                    del jsonObj[key][k]

    # Next modify the date
    if datetoggle == False:
        jsonObj["date"] = jsonObj["date"]["sdate"]
    else:
        l = []
        start = jsonObj["date"]["start"].encode('unicode-escape')
        end = jsonObj["date"]["end"].encode('unicode-escape')
        l.append(str({"start": start, "end": end}))
        jsonObj["date"] = l

    # Start an html list
    htmlResult = "<ul>"
    # Trim whitespace from the values of the json object
    for key, value in jsonObj.iteritems():
        # The value is a string
        if isinstance(value, basestring):
            stripped = value.strip(' \t\n\r')
            htmlResult += "<li><b>" + key + "</b>: " + stripped + "</li>"
        # The value is a list
        else:
            stripped = []
            htmlResult += "<li><b>" + key + "</b>:<ul>"
            for item in value:
                item = item.strip(' \t\n\r')
                stripped.append(item)
                htmlResult += "<li>" + item + "</li>"
            htmlResult += "</ul></li>"
        jsonObj[key] = stripped
    htmlResult += "</ul>"
    # The html has to be packaged in the json object for Flask to return it in the response.
    # Move the rest of the json for the database to another variable.
    jsonForDB = jsonObj
    htmlResult = {"htmlResult": htmlResult}
    jsonObj.update(htmlResult)
    jsonResult = json.dumps(jsonObj, sort_keys=False, indent=4, separators=(',', ': '))

    # Change slashes to commas in the path
    jsonForDB["path"] = jsonForDB["path"].replace("/", ",")
    jsonforDB = json.dumps(jsonForDB, sort_keys=False, indent=4, separators=(',', ': '))

    # Build a pymongo command to insert the data in the database. This should probably be moved 
    # to a separate function. Database data will not be saved unless active is set to True.
    active = True
    if active == True:
        client = MongoClient(db_config)
        db = client['Corpus']
        corpus = db['Corpus']
        # Straightforward insert -- publications.insert(jsonForDB)
        # Upsert is better because it works for add and edit
        id = jsonForDB.pop("_id")
        corpus.update({"_id": id}, {"$set": jsonforDB}, upsert=True)

    # Return the Ajax response
    return jsonResult


##########################
### Deletion Functions ###
##########################
@app.route("/delete", methods=["GET", "POST"])
def delete():
    """
    Deletes a document from the database. Mode is passed in headers.
    """
    id = request.data
    # Build a pymongo command to delete the document by _id. Only executes if active is set to True.
    active = True
    mode = request.headers["mode"]
    client = MongoClient(db_config)
    if active == True:
        # Switch mode
        if request.headers["mode"] == "deleteCollectionNode":
            db = client['Corpus']
            node = db['Corpus']
            # elif request.headers["mode"] == "something else:
            # db = client['Something']
            # node = db['Something']
        else:
            db = client['Publications']
            node = db['Publications']
        node.remove({"_id": id})
    # Return the Ajax response
    return "Success."


###################
### Run the app ###
###################
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
