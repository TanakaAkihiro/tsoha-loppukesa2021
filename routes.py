from logging import error
from app import app
from flask import render_template, request, redirect, session
import users, threads, messages, visits, likes

@app.route("/")
def index():
    list = threads.get_list()
    message_counter = threads.get_message_counts()
    visit_counter = visits.get_counter()
    return render_template("index.html", threads=list, message_counts=message_counter, visit_counts=visit_counter)

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
    message_list = messages.get_list(id)
    like_list = likes.get_list(id)
    visits.add_visit(id)
    return render_template("thread.html", messages=message_list, likes=like_list, thread=threads.topic(id))

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
        return redirect("/thread/"+str(messages.get_thread_id(id)))
    return render_template("error.html", error="Viestin poistaminen epäonnistui")

@app.route("/search_result", methods=["POST"])
def search_result():
    query = request.form["query"]
    result = messages.search(query)
    return render_template("search_result.html", messages=result)

@app.route("/like/<int:thread_id>/<int:message_id>")
def like_message(thread_id, message_id):
    if not likes.check_if_liked_before(session["user_id"], message_id):
        likes.like_message(session["user_id"],message_id)
    else:
        if likes.update_like(session["user_id"], message_id):
            return redirect("/thread/"+str(thread_id))
        else:
            return render_template("error.html", error="Tykkääminen/tykkäyksen poistaminen epäonnistui")
        