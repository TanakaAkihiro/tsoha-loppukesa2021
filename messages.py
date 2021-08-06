from db import db
import users, threads

def get_list(thread_id):
    sql = """SELECT M.id, M.user_id, M.content, M.created_at, M.visible, U.username 
        FROM messages M, threads T JOIN users U ON U.id=T.user_id WHERE T.id=:thread_id"""
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchall()