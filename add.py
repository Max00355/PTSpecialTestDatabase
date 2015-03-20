from flask import Blueprint, request, render_template, redirect
import mongo
from bson import ObjectId

add = Blueprint("add", __name__)
add.jinja_autoescape = False

@add.route("/add/<_id>", methods=['GET', 'POST'])
def method2(_id):
    if request.remote_addr != "127.0.0.1":
        return "404 Page not found.", 404
    _id = ObjectId(_id)
    if request.method == "POST":
        bodyPart = request.form['body_part'].lower()
        name = request.form['test_name']
        keywords = request.form['keywords'].lower().split(",")
        summary = request.form['summary']
        procedure = request.form['procedure']
        articles = request.form['articles']
        data = [x for x in mongo.db.enteries.find()]
        found = False
        for x in data:
            if x['testName'].lower() == name.lower():
                found = True
                mongo.db.enteries.update({"testName":x['testName']}, {"bodyPart":bodyPart, "testName":name, "keywords":keywords, "summary":summary, "procedure":procedure, "articles":articles})
                break
        if not found:
            mongo.db.enteries.insert({"bodyPart":bodyPart, "testName":name, "keywords":keywords, "summary":summary, "procedure":procedure, "articles":articles})
        return redirect("/test/{}".format(_id))

    data = mongo.db.enteries.find_one({"_id":_id})
    summary = data['summary']
    procedure = data['procedure']
    keywords = ','.join(data['keywords'])
    test_name = data['testName']
    articles = data['articles']
    
    
    return render_template("add.html",summary=summary, procedure=procedure, keywords=keywords, test_name=test_name, articles=articles)


@add.route("/add/", methods=['GET', 'POST'])
def method():
    if request.remote_addr != "127.0.0.1":
        return "404 Page not found.", 404

    if request.method == "POST":
        bodyPart = request.form['body_part'].lower()
        name = request.form['test_name']
        keywords = request.form['keywords'].lower().split(",")
        summary = request.form['summary']
        procedure = request.form['procedure']
        articles = request.form['articles']
        data = [x for x in mongo.db.enteries.find()]
        found = False
        for x in data:
            if x['testName'].lower() == name.lower():
                found = True
                mongo.db.enteries.update({"testName":x['testName']}, {"bodyPart":bodyPart, "testName":name, "keywords":keywords, "summary":summary, "procedure":procedure, "articles":articles})
                break
        if not found:
            mongo.db.enteries.insert({"bodyPart":bodyPart, "testName":name, "keywords":keywords, "summary":summary, "procedure":procedure, "articles":articles})
        return redirect("/test/{}".format(_id))

    return render_template("add.html")
