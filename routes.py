from logging import error
from app import app
from flask import render_template, request, redirect, session
import users, threads
#import messages

@app.route("/")
def index():
    list = threads.get_list()
    return render_template("index.html", threads=list)

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

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        session["username"] = username
        return redirect("/")
    return render_template("error.html", error="Väärä käyttäjätunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/new_thread")
def new_thread():
    return render_template("new_thread.html")

@app.route("/create_thread", methods=["POST"])
def create_thread():
    topic = request.form["topic"]
    if threads.create(session["user_id"], topic):
        return redirect("/")
    return render_template("error.html", error="Uuden keskustelun luominen epäonnistui")
    