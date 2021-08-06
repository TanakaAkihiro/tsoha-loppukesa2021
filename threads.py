from db import db
import users

def get_list():
    sql = """SELECT T.id, T.topic, T.created_at, T.visible, U.username, U.role FROM threads T, users U 
            WHERE T.user_id=U.id ORDER BY T.id"""
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
    sql = "SELECT topic FROM threads WHERE id=:id"
    return db.session.execute(sql, {"id":id}).fetchone()