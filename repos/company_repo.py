from db import get_db

def create_company(user_id, company_name, created_at):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO companies (user_id, company_name, created_at)
        VALUES(?, ?, ?)
        """,
        (user_id, company_name, created_at)
    )

    conn.commit()
    conn.close()

def list_companies_by_users(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, user_id, company_name, created_at
        FROM companies
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return rows

def get_company_by_name_for_user(user_id, company_name):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, user_id, company_name, created_at
        FROM companies
        WHERE user_id = ? AND company_name = ?
        """,
        (user_id, company_name)
    )

    row = cursor.fetchone()
    conn.close()

    return row

def get_company_by_id_for_user(user_id, company_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, user_id, company_name, created_at
        FROM companies
        WHERE id = ? AND user_id = ?
        """,
        (company_id, user_id)
    )

    row = cursor.fetchone()
    conn.close()

    return row