from logging import error
from app import app
from flask import render_template, request, redirect, session
import users
#import messages

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/new_account")
def new_account():
    return render_template("new_account.html")

@app.route("/create_account", methods=["POST"])
def create_account():
    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]
    users.register(username, password, role)
    return redirect("/")