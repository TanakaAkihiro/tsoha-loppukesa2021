from db import db


def get_counts(thread_id):
    sql = """SELECT M.id as message_id, COUNT(case when L.bool=true then 1 end)
        FROM messages M LEFT JOIN threads T ON M.thread_id=T.id LEFT JOIN likes L ON L.message_id=M.id
        WHERE M.visible=true AND T.visible=true AND T.id=:thread_id
        GROUP BY M.id ORDER BY M.id"""
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchall()

def get_list(user_id):
    sql = """SELECT M.id as message_id, L.bool
        FROM messages M LEFT JOIN likes L ON L.message_id=M.id
        WHERE L.user_id=:user_id OR L.user_id IS NULL"""
    result = db.session.execute(sql, {"user_id":user_id})
    return result.fetchall()

def like_message(user_id, message_id):
    sql = "INSERT INTO likes (user_id, message_id, bool) VALUES (:user_id, :message_id, true)"
    db.session.execute(sql, {"user_id":user_id, "message_id":message_id})
    db.session.commit()

def check_if_liked_before(user_id, message_id):
    sql = "SELECT * FROM likes WHERE user_id=:user_id AND message_id=:message_id"
    result = db.session.execute(sql, {"user_id":user_id, "message_id":message_id}).fetchone()
    if result is None:
        return False
    return True

def update_like(user_id, message_id):
    sql = "UPDATE likes SET bool=not bool WHERE user_id=:user_id AND message_id=:message_id"
    db.session.execute(sql, {"user_id":user_id, "message_id":message_id})
    db.session.commit()