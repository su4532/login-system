# import ssl
#
# import certifi
# ca = certifi.where()

import datetime

import os
from dotenv import load_dotenv
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template, request, redirect, url_for, flash, session
from passlib.hash import sha256_crypt

load_dotenv()
uri = os.getenv("MONGO_URI")

print("hello")
# Create a new client and connect to the server
# client = MongoClient(uri, tlsCAFile=ca, server_api=ServerApi("1"))
# client = MongoClient(uri, ssl_cert_reqs=ssl.CERT_NONE, server_api=ServerApi("1"))
client = MongoClient(uri, server_api=ServerApi("1"))

print("client created")

db = client["youngwonks_database"]

# login_info = db.login.insert_one({"first_name": "first", "last_name": "last", "email": "email_address", "password": "password"})
# print(login_info)

app = Flask("Login System")
app.secret_key = sha256_crypt.hash("secret key")

@app.route("/", methods=["GET", "POST"])
def index():
    # if request.method == "GET":
    #     notes = db.notes.find()
    #     return render_template("index.html", notes=notes)
    if request.method == "POST":
        if "signup_button" in request.form:
            encrypted_password = sha256_crypt.hash(request.form["signup_password"])
            app.secret_key = encrypted_password
            db.login.insert_one({"first_name": request.form["signup_first"], "last_name": request.form["signup_last"],
                                 "email": request.form["signup_email"], "password": encrypted_password})
        elif "login_button" in request.form:
            user = db.login.find_one({"email": request.form["email_address"]})
            if user:
                user_password = request.form["login_password"]
                if sha256_crypt.verify(user_password, user["password"]):
                    session["email"] = user["email"]
                    return redirect("/home")
                else:
                    flash("Incorrect password. Try again.")
            else:
                flash("Account doesn't exist. Please sign up.")
                return redirect("/")
        print(request.form)
        return redirect("/")

    return render_template("index.html")


@app.route("/home", methods=["GET", "POST"])
def home():
    if "email" in session:
        return render_template("home.html")
    else:
        flash("Please login first.")
        return redirect("/")


@app.route("/logout")
def logout():
    del session["email"]
    flash("You are now logged out.")
    return redirect("/")

# @app.route("/delete/<note_id>", methods=["GET", "POST"])
# def delete_noteid(note_id):
#     db.notes.delete_one({"_id": ObjectId(note_id)})
#     return redirect("/")

app.run(debug=True, host='0.0.0.0')
