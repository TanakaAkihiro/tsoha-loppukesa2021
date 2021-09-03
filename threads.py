from db import db
import users

def get_list():
    sql = """SELECT T.id, T.topic, T.created_at, T.visible, U.username, U.role 
        FROM threads T, users U 
        WHERE T.user_id=U.id AND T.visible=true ORDER BY T.id"""
    result = db.session.execute(sql)
    return result.fetchall()

def create(user_id, topic):
    sql = """INSERT INTO threads (user_id, topic, created_at, visible) VALUES (:user_id, :topic, NOW(), true)"""
    try:
        db.session.execute(sql, {"user_id":user_id, "topic":topic})
        db.session.commit()
    except:
        return False
    return True

def delete(id, user_id, user_role):
    sql = "SELECT user_id FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id":id})
    if result.fetchone().user_id == user_id or user_role == 2:
        sql = "UPDATE threads SET visible = false WHERE id=:id"
        db.session.execute(sql, {"id":id})
        db.session.commit()
        return True
    return False

def topic(id):
    sql = "SELECT T.id, T.topic, U.username FROM threads T, users U WHERE T.user_id=U.id AND T.id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()

def get_message_counts():
    sql = """SELECT T.id as thread_id, COUNT(M.id) 
        FROM messages M, threads T
        WHERE M.thread_id=T.id AND M.visible=true 
        GROUP BY T.id ORDER BY T.id"""
    return db.session.execute(sql).fetchall()

def update(id, topic):
    sql = "UPDATE threads SET topic=:topic WHERE id=:id"
    try:
        db.session.execute(sql, {"id":id, "topic":topic})
        db.session.commit()
        return True
    except:
        return False