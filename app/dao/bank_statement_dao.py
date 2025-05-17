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
    cur.execute(
        """
        INSERT INTO bank_statements (date, account_number)
        VALUES (?, ?)
        """,
        (date, account_number),
    )
    return cur.lastrowid


def list_bank_statements(
    account_number, limit=10, offset=0, date_from=None, date_to=None, sort=None
):
    if not account_number:
        return []

    cur = get_cursor()

    # Build WHERE clause
    where_clauses = ["account_number = ?"]
    params = [account_number]

    if date_from:
        where_clauses.append("date >= ?")
        params.append(date_from)
    if date_to:
        where_clauses.append("date <= ?")
        params.append(date_to)

    where_sql = " WHERE " + " AND ".join(where_clauses)

    # Build ORDER BY clause
    if sort:
        order_clauses = [
            f"{s[1:]} DESC" if s.startswith("-") else f"{s} ASC" for s in sort
        ]
        order_sql = " ORDER BY " + ", ".join(order_clauses)
    else:
        order_sql = " ORDER BY date DESC"

    # Final SELECT query with pagination
    query = f"SELECT * FROM bank_statements{where_sql}{order_sql} LIMIT ? OFFSET ?"
    cur.execute(query, params + [limit, offset])
    rows = [dict(row) for row in cur.fetchall()]

    # Total count query
    count_query = f"SELECT COUNT(*) FROM bank_statements{where_sql}"
    cur.execute(count_query, params)
    total = cur.fetchone()[0]

    return {
        "rows": rows,
        "total": total,
        "offset": offset,
        "limit": limit,
    }


def delete_bank_statement(bank_statement_id, date=None, account_number=None):
    bs = get_bank_statement(
        bank_statement_id=bank_statement_id, date=date, account_number=account_number
    )

    if not bs:
        return None

    cur = get_cursor()

    cur.execute(
        """
        DELETE FROM bank_statements
        WHERE id = ?
        """,
        (bank_statement_id,),
    )
    return cur.rowcount > 0
