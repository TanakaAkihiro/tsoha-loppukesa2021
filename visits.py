from db import db

def add_visit(thread_id):
    sql = "INSERT INTO visits (thread_id, visited_at) VALUES (:thread_id, NOW())"
    db.session.execute(sql, {"thread_id":thread_id})
    db.session.commit()

def get_counter():
    result = db.session.execute("SELECT thread_id, COUNT(*) FROM visits GROUP BY thread_id")
    return result.fetchall()
