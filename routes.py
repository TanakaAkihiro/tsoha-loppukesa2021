from logging import error
from app import app
from flask import render_template, request, redirect, session
import users, threads, messages, visits, likes

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
    password_2 = request.form["password_2"]
    if users.check_if_existed(username):
        return render_template("error.html", error="Käyttäjänimi on varattu")
    elif password!= password_2:
        return render_template("error.html", error="Salasanat eroavat toisistaan")
    elif len(username) > 50 or len(username) < 7:
        return render_template("error.html", error="Käyttäjänimen pituuden tulee olla 8-50 merkin pituinen")
    elif len(password) > 100 or len(password) < 7:
        return render_template("error.html", error="Salasanan pituuden tulee olla 8-100 merkin pituinen")
    role = request.form["role"]
    if not users.register(username, password, role):
        return render_template("error.html", error="Uuden käyttäjän luominen epäonnistui")
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
    users.check_csrf(request.form["csrf_token"])
    topic = request.form["topic"]
    if len(topic) > 100:
        return render_template("error.html", error="Aihe on liian pitkä")
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
    like_counts = likes.get_counts(id)
    like_list = likes.get_list(session["user_id"])
    visits.add_visit(id)
    return render_template("thread.html", messages=message_list, like_counts=like_counts, likes=like_list, thread=threads.topic(id))

@app.route("/edit_thread/<int:thread_id>")
def edit_thread(thread_id):
    thread = threads.topic(thread_id)
    return render_template("edit_thread.html", thread=thread)

@app.route("/update_thread/<int:thread_id>", methods=["GET", "POST"])
def update_thread(thread_id):
    users.check_csrf(request.form["csrf_token"])
    topic = request.form["topic"]
    if len(topic) > 100:
        return render_template("error.html", error="Aihe on liian pitkä")
    if threads.update(thread_id, topic):
        return redirect("/")
    return render_template("error.html", error="Aiheen muokkaaminen epäonnistui")

@app.route("/new_message/<int:thread_id>")
def new_message(thread_id):
    return render_template("new_message.html", thread=threads.topic(thread_id))

@app.route("/create_message/<int:thread_id>", methods=["POST"])
def create_message(thread_id):
    users.check_csrf(request.form["csrf_token"])
    content = request.form["content"]
    if len(content) > 5000:
        return render_template("error.html", error="Viesti on liian pitkä")
    if messages.create(session["user_id"], thread_id, content):
        return redirect("/thread/"+str(thread_id))
    return render_template("error.html", error="Uuden viestin lähettäminen epäonnistui")

@app.route("/delete_message/<int:id>", methods=["GET", "POST"])
def delete_message(id):
    if messages.delete(id, session["user_id"], session["user_role"]):
        return redirect("/thread/"+str(messages.get_thread_id(id)))
    return render_template("error.html", error="Viestin poistaminen epäonnistui")

@app.route("/edit_message/<int:message_id>")
def edit_message(message_id):
    message = messages.get_content(message_id)
    return render_template("edit_message.html", message=message)

@app.route("/update_message/<int:message_id>", methods=["GET", "POST"])
def update_message(message_id):
    users.check_csrf(request.form["csrf_token"])
    content = request.form["content"]
    if len(content) > 5000:
        return render_template("error.html", error="Viesti on liian pitkä")
    if messages.update(message_id, content):
        return redirect("/thread/"+str(messages.get_thread_id(message_id)))
    return render_template("error.html", error="Viestin muokkaaminen epäonnistui")

@app.route("/search_result", methods=["POST"])
def search_result():
    query = request.form["query"]
    result = messages.search(query)
    return render_template("search_result.html", messages=result, keyword=query)

@app.route("/like/<int:thread_id>/<int:message_id>")
def like_message(thread_id, message_id):
    if not likes.check_if_liked_before(session["user_id"], message_id):
        likes.like_message(session["user_id"],message_id)
        return redirect("/thread/"+str(thread_id))
    else:
        if likes.update_like(session["user_id"], message_id):
            return redirect("/thread/"+str(thread_id))
        else:
            return render_template("error.html", error="Tykkääminen/tykkäyksen poistaminen epäonnistui")