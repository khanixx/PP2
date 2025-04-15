from connect import connect

def create_user(username):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO users (username) VALUES (%s) ON CONFLICT DO NOTHING", (username,))
            conn.commit()

def get_user(username):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            return user[0] if user else None

def get_last_score(username):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT score, level FROM user_scores 
                WHERE user_id = (SELECT id FROM users WHERE username = %s)
                ORDER BY created_at DESC LIMIT 1
            """, (username,))
            return cur.fetchone()

def save_score(username, score, level):
    with connect() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            user_id = cur.fetchone()[0]
            cur.execute("INSERT INTO user_scores (user_id, score, level) VALUES (%s, %s, %s)",
                        (user_id, score, level))
            conn.commit()
