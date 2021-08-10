from logging import error
from app import app
from flask import render_template, request, redirect, session
import users, threads, messages

@app.route("/")
def index():
    list = threads.get_list()
    count_list = threads.get_message_counts()
    return render_template("index.html", threads=list, counts=count_list)

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

@app.route("/delete_thread/<int:id>", methods=["GET", "POST"])
def delete_thread(id):
    if threads.delete(id, session["user_id"], session["user_role"]):
        return redirect("/")
    return render_template("error.html", error="Keskusteluketjun poistaminen epäonnistui")

@app.route("/thread/<int:id>")
def thread(id):
    list = messages.get_list(id)
    return render_template("thread.html", messages=list, thread=threads.topic(id))

@app.route("/new_message/<int:thread_id>")
def new_message(thread_id):
    return render_template("new_message.html", thread=threads.topic(thread_id))

@app.route("/create_message/<int:thread_id>", methods=["POST"])
def create_message(thread_id):
    content = request.form["content"]
    if messages.create(session["user_id"], thread_id, content):
        return redirect("/thread/"+str(thread_id))
    return render_template("error.html", error="Uuden viestin lähettäminen epäonnistui")

@app.route("/delete_message/<int:id>", methods=["GET", "POST"])
def delete_message(id):
    if messages.delete(id, session["user_id"], session["user_role"]):
        print("jej")
        return redirect("/thread/"+str(messages.get_thread_id(id)))
    return render_template("error.html", error="Viestin poistaminen epäonnistui")
