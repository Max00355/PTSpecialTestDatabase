from flask import Blueprint, render_template, redirect, request
import mongo
from bson import ObjectId

page = Blueprint("page", __name__)
page.auto_escape = False

@page.route("/test/<_id>", methods=['GET', 'POST'])
def method(_id):
    if request.method == "POST":
        return redirect("/search/{0}".format(request.form['search']))
    return render_template("page.html", data=mongo.db.enteries.find_one({"_id":ObjectId(_id)}))
