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
    if rawSearch:
        bodyPart = rawSearch['bodyPart']
    
    baseKeys = {
        "spine":["lumbar", "cervical", "spine", "lower back", "upper back", "mid back", "middle back", "back"],

    }
    
    for part in baseKeys:
        for altName in baseKeys[part]:
            if altName in search and not bodyPart:
                bodyPart = part
                break
        if bodyPart: break 
     
    if bodyPart:
        search = search.replace(altName, bodyPart)
     
    if not bodyPart:    
        rawData = mongo.db.enteries.find()
    else:
        rawData = mongo.db.enteries.find({"bodyPart":bodyPart})
    ranking = []
    for i in rawData:
        keyWords = i['keywords']
        rank = 0
        for x in keyWords:
            if search.find(x.lower()) != -1:
                rank += 1
        if rank != 0:
            ranking.append((rank, i))
        
    data = sorted(ranking)
    data.reverse()
    if not data:
        if not rawSearch:
            data = [(0, {"testName":"No tests found"})]
        else:
            data = [(0, x) for x in mongo.db.enteries.find()]
            
    if rawSearch:
        for x in range(len(data)):
            if data[x][1] == rawSearch:
                data.pop(x)
                break
    
        data = [(0, rawSearch)] + data

    return render_template("search.html", data=data, results=len(data))

