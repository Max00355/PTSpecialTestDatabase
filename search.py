from flask import Blueprint, render_template, redirect, request
import mongo
import string
import re

search = Blueprint("search", __name__)

@search.route("/", methods=['GET', 'POST'])
def method():
    if request.method == "POST":
        return redirect("/search/{0}".format(request.form['search']))
    return render_template("index.html")

@search.route("/search/<search>", methods=['GET', 'POST'])
def method_search(search):

    if request.method == "POST":
        return redirect("/search/{0}".format(request.form['search']))


    for x in string.punctuation:
        search = search.replace(x, '')
        
    search = search.lower().split()
    filterWords = ["is", "when", "this", "but", "and", "the", "so", "it", "to", "too", "a", "i"]
    for x in filterWords:
        while x in search:
            search.remove(x)
    search = ' '.join(search)
    bodyPart = None
    rawSearch = mongo.db.enteries.find_one({"testName":{"$regex":search, "$options":"-i"}})
    results = 0

    if rawSearch: # If the search is an exact match to some test in the database
        bodyPart = rawSearch['bodyPart']
        results += 1

    baseKeys = {
        "spine":["lumbar", "cervical", "spine", "lower back", "upper back", "mid back", "middle back", "back", "sacrum", "sacro"],
        "knee":["patella", "popliteal", "knee"],
        "shoulder":["shoulder", "rotator cuff"],
        "elbow":["olecranon", "elbow"],
        "wrist":["wrist", "hand"],
        "hip":["hip", "pelvis", "pelvic", "sacro", "sacrum", "labrum", "labral"]
    }
    
    for part in baseKeys:
        for altName in baseKeys[part]:
            if altName in search and not bodyPart:
                bodyPart = part
                break
        if bodyPart: break 
     
    if bodyPart:
        search = search.replace(altName, bodyPart)
    
    if bodyPart:
        nextSearch = mongo.db.enteries.find({"bodyPart":bodyPart})
    else:
        nextSearch = mongo.db.enteries.find()

    data = [] #(numOfMatches, data)
    
    # This is the ranking algorithm. We traverse the nextSearch array and find the number of matching keywords in the raw search.
    # The number of matches is recorded and compared against other enteries in the data array. A minimum of 25 tests are returned and they are ranked by the number of keyword matches.

    for s in nextSearch:
        matches = 0
        for keyword in s['keywords']:
            if keyword in search:
                matches += 1
        if len(data) < 25:
            data.append((matches, s))
            data = sorted(data, key=lambda x: x[0])
        else:
            if matches > data[0][0]:
                data.pop(0)
                data.append((matches, s))
                data = sorted(data, key=lambda x: x[0])
    
    results = results + len(data)
    data.reverse()

    return render_template("search.html", data=data, results=results, exactFind=rawSearch)

