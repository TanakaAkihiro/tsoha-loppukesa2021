from db import db


def get_list(thread_id):
    sql = """SELECT L.message_id, COUNT(*) FROM likes L, messages M, threads T 
    WHERE L.message_id=M.id AND M.thread_id=T.id AND M.visible=true AND T.visible=true AND L.bool=true AND T.id=:thread_id GROUP BY L.message_id ORDER BY L.message_id"""
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchall()