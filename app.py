import re
from typing import Collection
from urllib.parse import uses_fragment
from dns.rdatatype import NULL
from pymongo import MongoClient, collection
from bson.objectid import ObjectId
import certifi
from flask import Flask,render_template, request, redirect

app=Flask(__name__)

client=MongoClient("mongodb+srv://ZoranZheng:Zzh604089@cluster0.d6knc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",tlsCAFile=certifi.where())
db=client.contacts
# store the userName and password
userManager=db.userManager

@app.route("/")
def main():
    return render_template("log_in.html")

# log in and sign up logic 
@app.route("/contacts", methods=["POST"])
def showContacts():
    action=request.values.get("action")
    userName=request.values.get("userName")
    password=request.values.get("password")
    # whether the userName exists
    exist=userManager.find_one({"userName":userName})
    if action=="Sign up":
        if exist==None:
            userManager.insert_one({"userName":userName,"password":password})
        return render_template("signUp.html",exist=exist)
    else:
        contacts=db[userName].find()
        return render_template("contacts.html",password=password,exist=exist,contacts=contacts)

# add new contact
@app.route("/contacts/new")
def addNew():
    userName=request.args.get("userName")
    return render_template("new.html",userName=userName)


@app.route("/contacts/new", methods=["POST"])
def addIn():
    name=request.values.get("name")
    phone=request.values.get("phone")     
    address=request.values.get("address")
    userName=request.args.get("userName")
    collection=db[userName]
    collection.insert_one({"name":name,"phone":phone,"address":address})
    # find the userName's collection
    contacts=collection.find()
    return render_template("showData.html",contacts=contacts,userName=userName)


@app.route("/contacts/<id>", methods=['GET'])
def edit(id):
    id=request.view_args["id"]
    userName=request.args.get("userName")
    contact=db[userName].find_one(ObjectId(id))
    return render_template("edit.html",contact=contact, userName=userName)

@app.route("/contacts/edit/<id>", methods=["POST"])
def update(id):
    name=request.values.get("name")
    phone=request.values.get("phone")     
    address=request.values.get("address")
    id=request.view_args["id"]
    userName=request.args.get("userName")
    contacts=db[userName].find()
    contact=db[userName].update_one({"_id":ObjectId(id)},{"$set": {"name":name,"phone":phone,"address":address}})
    return render_template("showData.html",contacts=contacts,userName=userName)

@app.route("/contacts/delete/<id>", methods=['GET'])
def delete(id):
    userName=request.args.get("userName")
    contacts=db[userName].find()
    id=request.view_args["id"]
    db[userName].delete_one({"_id":ObjectId(id)})
    return render_template("showData.html",contacts=contacts,userName=userName)

@app.route("/contacts/<userName>/search", methods=['POST'])
def search(userName):
    id=request.view_args["userName"]
    print(userName)
    searchName=request.values.get("name")
    contact=db[userName].find_one({"name":searchName})
    return render_template("search.html",contact=contact,userName=userName)

if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0")