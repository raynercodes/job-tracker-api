from db import get_db

def create_application(user_id, company_id, job_title, notes, status, applied_at, created_at):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO applications (
            user_id,
            company_id,
            job_title,
            notes,
            status,
            applied_at,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (user_id, company_id, job_title, notes, status, applied_at, created_at)
    )
    
    conn.commit()
    conn.close()

def list_applications_by_user(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT applications.id,
        applications.user_id,
        applications.company_id,
        companies.company_name,
        applications.job_title,
        applications.notes,
        applications.status,
        applications.applied_at,
        applications.created_at
        FROM applications
        JOIN companies ON companies.id = applications.company_id
        WHERE applications.user_id = ?
        ORDER BY applications.created_at DESC
        """,
        (user_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return rows

def get_application_by_id_for_user_repo(user_id, application_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT applications.id,
        applications.user_id,
        applications.company_id,
        companies.company_name,
        applications.job_title,
        applications.notes,
        applications.status,
        applications.applied_at,
        applications.created_at
        FROM applications
        JOIN companies ON companies.id = applications.company_id
        WHERE applications.user_id = ? AND applications.id = ?
        """,
        (user_id, application_id)
    )

    rows = cursor.fetchone()
    conn.close()

    return rows

def update_application_for_user_repo(user_id, application_id, company_id, job_title, notes, status, applied_at):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE applications
        SET company_id = ?,
        job_title = ?,
        notes = ?,
        status = ?,
        applied_at = ?
        WHERE user_id = ? AND id = ?
        """,
        (company_id, job_title, notes, status, applied_at, user_id, application_id)
    )

    conn.commit()
    conn.close()

def delete_application_for_user_repo(user_id, application_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM applications
        WHERE user_id = ? AND id = ?
        """,
        (user_id, application_id)
    )

    conn.commit()
    conn.close()

def list_applications_by_user_with_filters_repo(user_id, status=None, company_id=None):
    conn = get_db()
    cursor = conn.cursor()

    base_query = """
    SELECT applications.id,
    applications.user_id,
    applications.company_id,
    companies.company_name,
    applications.job_title,
    applications.notes,
    applications.status,
    applications.applied_at,
    applications.created_at
    FROM applications
    JOIN companies ON companies.id = applications.company_id
    WHERE 1=1 
    """

    params = []

    base_query += " AND applications.user_id = ?"
    params.append(user_id)

    if status:
        base_query += " AND applications.status = ?"
        params.append(status)

    if company_id is not None:
        base_query += " AND applications.company_id = ?"
        params.append(company_id)

    base_query += " ORDER BY applications.created_at DESC"

    cursor.execute(base_query, params)

    rows = cursor.fetchall()
    conn.close()

    return rows

def get_application_stats_for_user_repo(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT status, COUNT(*)
        FROM applications
        WHERE user_id = ?
        GROUP BY status
        """,
        (user_id,)
    )

    rows = cursor.fetchall()

    conn.close()
    return rows