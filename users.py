import os
from flask import abort, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import db

def login(username, password):
    sql = "SELECT password, id, role FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user[0], password):
        session["user_id"] = user[1]
        session["username"] = user[0]
        session["user_role"] = user[2]
        session["csrf_token"] = os.urandom(16).hex()
        return True
    return False

def logout():
    del session["user_id"]
    del session["username"]
    del session["user_role"]

def register(username, password, role):
    hash_value = generate_password_hash(password)
    try:
        sql = """INSERT INTO users (username, password, role)
                VALUES (:username, :password, :role)"""
        db.session.execute(sql, {"username":username, "password":hash_value, "role":role})
        db.session.commit()
    except:
        return False
    return True

def check_if_existed(username):
    sql = "SELECT COUNT(*) FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username}).fetchone()
    if result[0] == 0:
        return False
    return True

def user_id():
    return session.get("user_id", 0)

def require_role(role):
    if role > session.get("user_role", 0):
        abort(403)

def check_csrf(csrf):
    if session["csrf_token"] != csrf:
        abort(403)
