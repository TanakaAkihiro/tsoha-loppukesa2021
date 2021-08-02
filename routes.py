from app import app
from flask import render_template, request, redirect
#import messages, users

@app.route("/")
def index():
    return render_template("index.html")