from app.utils.db import get_cursor


def get_bank_statement(bank_statement_id=None, date=None, account_number=None):
    # Must provide either an ID, or both date + account_number
    if not bank_statement_id and (not date or not account_number):
        return None

    cur = get_cursor()
    query = "SELECT * FROM bank_statements WHERE 1=1"
    params = []

    if bank_statement_id:
        query += " AND id = ?"
        params.append(bank_statement_id)

    if date:
        query += " AND date = ?"
        params.append(date)

    if account_number:
        query += " AND account_number = ?"
        params.append(account_number)

    cur.execute(query, params)
    row = cur.fetchone()
    return dict(row) if row else None


# --- Bank Statements CRUD ---
def create_bank_statement(date, account_number):
    cur = get_cursor()
    print(f"Creating bank statement for account: {account_number}")
    print(f"Statement date: {date}")
    cur.execute(
        """
        INSERT INTO bank_statements (date, account_number)
        VALUES (?, ?)
        """,
        (date, account_number),
    )
    return cur.lastrowid


def list_bank_statements(
    conn, limit=10, offset=0, q=None, date_from=None, date_to=None, sort=None
):
    cur = get_cursor()
    sql = "SELECT * FROM bank_statements WHERE 1=1"
    params = []
    if q:
        sql += " AND filename LIKE ?"
        params.append(f"%{q}%")
    if date_from:
        sql += " AND created_at >= ?"
        params.append(date_from)
    if date_to:
        sql += " AND created_at <= ?"
        params.append(date_to)
    if sort:
        for s in sort:
            if s.startswith("-"):
                sql += f" ORDER BY {s[1:]} DESC"
            else:
                sql += f" ORDER BY {s} ASC"
    else:
        sql += " ORDER BY created_at DESC"
    sql += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    cur.execute(sql, params)
    rows = cur.fetchall()
    return [dict(row) for row in rows]


def update_bank_statement(bank_statement_id, **kwargs):
    cur = get_cursor()
    fields = []
    values = []
    for k, v in kwargs.items():
        fields.append(f"{k} = ?")
        values.append(v)
    values.append(bank_statement_id)
    sql = f"UPDATE bank_statements SET {', '.join(fields)} WHERE id = ?"
    cur.execute(sql, values)
    return cur.rowcount


def delete_bank_statement(bank_statement_id):
    cur = get_cursor()
    cur.execute("DELETE FROM bank_statements WHERE id = ?", (bank_statement_id,))
    return cur.rowcount
