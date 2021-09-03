from db import db

def add_visit(thread_id):
    sql = "INSERT INTO visits (thread_id, visited_at) VALUES (:thread_id, NOW())"
    db.session.execute(sql, {"thread_id":thread_id})
    db.session.commit()
