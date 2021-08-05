from db import db
import users

def get_list():
    sql = """SELECT T.id, T.topic, U.username, T.created_at, T.visible FROM threads T, users U 
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