from db import db


def get_list(thread_id):
    sql = """SELECT M.id as message_id, COUNT(L.bool) FROM messages M LEFT JOIN threads T ON M.thread_id=T.id LEFT JOIN likes L ON L.message_id=M.id 
    WHERE M.visible=true AND T.visible=true AND T.id=:thread_id GROUP BY M.id ORDER BY M.id"""
    result = db.session.execute(sql, {"thread_id":thread_id})
    return result.fetchall()