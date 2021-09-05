from flask import render_template, request, redirect, session
from app import app
import users
import threads
import messages
import visits
import likes

@app.route("/")
def index():
    thread_list = threads.get_list()
    return render_template("index.html", threads=thread_list)

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
    if password!= password_2:
        return render_template("error.html", error="Salasanat eroavat toisistaan")
    if len(username) > 50 or len(username) < 7:
        return render_template("error.html", error="Käyttäjänimen pituuden tulee olla 8-50 merkin pituinen")
    if len(password) > 100 or len(password) < 7:
        return render_template("error.html", error="Salasanan pituuden tulee olla 8-100 merkin pituinen")
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
    users.check_csrf(request.form["csrf_token"])
    topic = request.form["topic"]
    if len(topic) > 100:
        return render_template("error.html", error="Aihe on liian pitkä")
    threads.create(session["user_id"], topic)
    return redirect("/")

@app.route("/delete_thread/<int:thread_id>", methods=["GET", "POST"])
def delete_thread(thread_id):
    if threads.delete(thread_id, session["user_id"], session["user_role"]):
        return redirect("/")
    return render_template("error.html", error="Keskusteluketjun poistaminen epäonnistui")

@app.route("/thread/<int:thread_id>")
def thread(thread_id):
    message_list = messages.get_list(thread_id)
    like_counts = likes.get_counts(thread_id)
    like_list = likes.get_list(session["user_id"])
    visits.add_visit(thread_id)
    return render_template("thread.html", messages=message_list, like_counts=like_counts, likes=like_list, thread=threads.get_topic(thread_id))

@app.route("/edit_thread/<int:thread_id>")
def edit_thread(thread_id):
    thread_topic = threads.get_topic(thread_id)
    return render_template("edit_thread.html", thread=thread_topic)

@app.route("/update_thread/<int:thread_id>", methods=["GET", "POST"])
def update_thread(thread_id):
    users.check_csrf(request.form["csrf_token"])
    topic = request.form["topic"]
    if len(topic) > 100:
        return render_template("error.html", error="Aihe on liian pitkä")
    threads.update(thread_id, topic)
    return redirect("/")

@app.route("/new_message/<int:thread_id>")
def new_message(thread_id):
    return render_template("new_message.html", thread=threads.get_topic(thread_id))

@app.route("/create_message/<int:thread_id>", methods=["POST"])
def create_message(thread_id):
    users.check_csrf(request.form["csrf_token"])
    content = request.form["content"]
    if len(content) > 5000:
        return render_template("error.html", error="Viesti on liian pitkä")
    messages.create(session["user_id"], thread_id, content)
    return redirect("/thread/"+str(thread_id))

@app.route("/delete_message/<int:message_id>", methods=["GET", "POST"])
def delete_message(message_id):
    if messages.delete(message_id, session["user_id"], session["user_role"]):
        return redirect("/thread/"+str(messages.get_thread_id(message_id)))
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
    messages.update(message_id, content)
    return redirect("/thread/"+str(messages.get_thread_id(message_id)))

@app.route("/search_result", methods=["POST"])
def search_result():
    query = request.form["query"]
    result = messages.search(query)
    return render_template("search_result.html", messages=result, keyword=query)

@app.route("/like/<int:thread_id>/<int:message_id>")
def like_message(thread_id, message_id):
    if not likes.check_if_liked_before(session["user_id"], message_id):
        likes.like_message(session["user_id"], message_id)
        return redirect("/thread/"+str(thread_id))
    likes.update_like(session["user_id"], message_id)
    return redirect("/thread/"+str(thread_id))

@app.route("/profile")
def profile():
    user_info = users.get_info(session["user_id"])
    return render_template("profile.html", user=user_info)