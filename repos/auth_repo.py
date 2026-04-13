from db import get_db

def create_user(username, password_hash, created_at):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
        (username, password_hash, created_at))

    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, password_hash
        FROM users
        WHERE username = ?
        """,
        (username,))
    
    row = cursor.fetchone()
    conn.close()
    return row

def store_refresh_token(user_id, token, created_at):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO refresh_tokens (user_id, token, created_at, revoked_at)
        VALUES (?, ?, ?, ?)
        """,
        (user_id, token, created_at, None)
    )

    conn.commit()
    conn.close()

def get_refresh_token_repo(token):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, user_id, token, created_at, revoked_at
        FROM refresh_tokens
        WHERE token = ?
        """,
        (token,)
    )

    row = cursor.fetchone()
    conn.close()

    return row
    
def revoke_refresh_token(token, revoked_at):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE refresh_tokens
        SET revoked_at = ?
        WHERE token = ?
        """,
        (revoked_at, token)
    )

    conn.commit()
    conn.close()