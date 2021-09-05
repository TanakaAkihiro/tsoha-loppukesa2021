from db import db

def get_list():
    sql = """
        SELECT T.id, T.topic, T.created_at, T.visible, U.username, U.role, X.count as message_count, Y.count as view_count
        FROM threads T
        LEFT JOIN users U
            ON T.user_id=U.id
        LEFT JOIN (
            SELECT A.id, COUNT(case when M.visible=true then 1 end)
            FROM threads A
            LEFT JOIN messages M
                ON M.thread_id=A.id
            GROUP BY A.id
            ORDER BY A.id
        ) X
            ON X.id=T.id
        LEFT JOIN (
            SELECT B.id, COUNT(V.id)
            FROM threads B
            LEFT JOIN visits V
                ON B.id=V.thread_id
            GROUP BY B.id
            ORDER BY B.id
        ) Y
            ON Y.id=T.id
        WHERE T.visible=true
        ORDER BY T.id"""
    result = db.session.execute(sql)
    return result.fetchall()

def create(user_id, topic):
    sql = """INSERT INTO threads (user_id, topic, created_at, visible) VALUES (:user_id, :topic, NOW(), true)"""
    db.session.execute(sql, {"user_id":user_id, "topic":topic})
    db.session.commit()

def delete(thread_id, user_id, user_role):
    sql = "SELECT user_id FROM threads WHERE id=:id"
    result = db.session.execute(sql, {"id":thread_id})
    if result.fetchone().user_id == user_id or user_role == 2:
        sql = "UPDATE threads SET visible = false WHERE id=:id"
        db.session.execute(sql, {"id":thread_id})
        db.session.commit()
        return True
    return False

def get_topic(thread_id):
    sql = """
    SELECT T.id, T.topic, U.username
    FROM threads T, users U
    WHERE T.user_id=U.id AND T.id=:id"""
    return db.session.execute(sql, {"id":thread_id}).fetchone()

def update(thread_id, topic):
    sql = "UPDATE threads SET topic=:topic WHERE id=:id"
    db.session.execute(sql, {"id":thread_id, "topic":topic})
    db.session.commit()
