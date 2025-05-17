from app.utils.db import get_cursor


def create_transaction(date, amount, description, balance, bank_statement_id=None):
    cur = get_cursor()
    cur.execute(
        """
        INSERT INTO transactions (date, amount, description, balance, bank_statement_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (date, amount, description, balance, bank_statement_id),
    )
    return cur.lastrowid


def get_transaction(transaction_id):
    cur = get_cursor()
    cur.execute("SELECT * FROM transactions WHERE id = ?", (transaction_id,))
    row = cur.fetchone()
    return dict(row) if row else None


def list_transactions(
    limit=10,
    offset=0,
    bank_statement_id=None,
    q=None,
    date_from=None,
    date_to=None,
    sort=None,
):
    cur = get_cursor()

    # Build WHERE clause dynamically
    conditions = []
    params = []

    if bank_statement_id:
        conditions.append("bank_statement_id = ?")
        params.append(bank_statement_id)

    if q:
        conditions.append("description LIKE ?")
        params.append(f"%{q}%")

    if date_from:
        conditions.append("date >= ?")
        params.append(date_from)

    if date_to:
        conditions.append("date <= ?")
        params.append(date_to)

    where_sql = f" WHERE {' AND '.join(conditions)}" if conditions else ""

    # Handle sorting
    if sort:
        order_sql = " ORDER BY " + ", ".join(
            f"{s[1:]} DESC" if s.startswith("-") else f"{s} ASC" for s in sort
        )
    else:
        order_sql = " ORDER BY date DESC"

    # Final SQL with pagination
    query = f"""
        SELECT * FROM transactions
        {where_sql}
        {order_sql}
        LIMIT ? OFFSET ?
    """
    paginated_params = params + [limit, offset]
    cur.execute(query, tuple(paginated_params))
    rows = [dict(row) for row in cur.fetchall()]

    # Get total count
    count_query = f"SELECT COUNT(*) FROM transactions {where_sql}"
    cur.execute(count_query, tuple(params))
    total = cur.fetchone()[0]

    return {
        "rows": rows,
        "total": total,
        "offset": offset,
        "limit": limit,
    }


def delete_transaction(transaction_id):
    cur = get_cursor()
    cur.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    return cur.rowcount


def delete_transactions_by_bank_statement(bank_statement_id):
    cur = get_cursor()
    cur.execute(
        "DELETE FROM transactions WHERE bank_statement_id = ?", (bank_statement_id,)
    )
    return cur.rowcount
