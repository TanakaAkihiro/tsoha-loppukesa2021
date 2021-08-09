from types import resolve_bases
from db import db
import users, threads

def get_list(thread_id):
    sql = """SELECT M.id, M.user_id, M.content, M.created_at, M.visible, T.id as thread_id, U.username 
        FROM messages M, threads T, users U WHERE M.thread_id=T.id AND M.user_id=U.id AND T.id=:thread_id"""
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchall()

def create(user_id, thread_id, content):
    sql = """INSERT INTO messages (user_id, thread_id, content, created_at, visible)
        VALUES (:user_id, :thread_id, :content, NOW(), true)"""
    try:
        db.session.execute(sql, {"user_id":user_id, "thread_id":thread_id, "content":content})
        db.session.commit()
    except:
        return False
    return True

def delete(id, user_id, user_role):
    sql = "SELECT user_id FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    if result.fetchone().user_id == user_id or user_role == 2:
        sql = "UPDATE messages SET visible = false WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    return False

def get_thread_id(id):
    sql = "SELECT thread_id FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    return result.fetchone().thread_id