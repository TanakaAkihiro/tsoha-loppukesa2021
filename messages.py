from db import db

def get_list(thread_id):
    sql = """
        SELECT M.id, M.user_id, M.content, M.created_at, M.visible, T.id as thread_id, U.username
        FROM messages M, threads T, users U
        WHERE M.thread_id=T.id AND M.user_id=U.id AND T.id=:thread_id AND M.visible=true
        ORDER BY M.id"""
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchall()

def create(user_id, thread_id, content):
    sql = """INSERT INTO messages (user_id, thread_id, content, created_at, visible)
        VALUES (:user_id, :thread_id, :content, NOW(), true)"""
    db.session.execute(sql, {"user_id":user_id, "thread_id":thread_id, "content":content})
    db.session.commit()

def delete(message_id, user_id, user_role):
    sql = "SELECT user_id FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id":message_id})
    if result.fetchone().user_id == user_id or user_role == 2:
        sql = "UPDATE messages SET visible = false WHERE id=:id"
        db.session.execute(sql, {"id":message_id})
        db.session.commit()
        return True
    return False

def get_content(message_id):
    sql = """SELECT M.id, M.content, M.thread_id, T.topic as thread_topic, U.username
        FROM messages M, threads T, users U
        WHERE M.thread_id=T.id AND M.user_id=U.id AND M.id=:id"""
    result = db.session.execute(sql, {"id":message_id})
    return result.fetchone()

def update(message_id, content):
    sql = "UPDATE messages SET content=:content WHERE id=:id"
    db.session.execute(sql, {"id":message_id, "content":content})
    db.session.commit()

def get_thread_id(message_id):
    sql = "SELECT thread_id FROM messages WHERE id=:id"
    result = db.session.execute(sql, {"id":message_id})
    return result.fetchone().thread_id

def search(query):
    sql = """SELECT M.id, M.content, M.created_at, U.username, T.topic
        FROM messages M, users U, threads T
        WHERE M.thread_id=T.id AND M.user_id=U.id AND M.content
        LIKE :query AND M.visible=true AND T.visible=true;"""
    return db.session.execute(sql, {"query":"%"+str(query)+"%"}).fetchall()
    