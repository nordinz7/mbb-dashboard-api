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


def list_transactions(limit=10, offset=0, bank_statement_id=None):
    cur = get_cursor()
    if bank_statement_id:
        cur.execute(
            "SELECT * FROM transactions WHERE bank_statement_id = ? ORDER BY date DESC LIMIT ? OFFSET ?",
            (bank_statement_id, limit, offset),
        )
    else:
        cur.execute(
            "SELECT * FROM transactions ORDER BY date DESC LIMIT ? OFFSET ?",
            (limit, offset),
        )
    rows = cur.fetchall()
    return [dict(row) for row in rows]


def update_transaction(transaction_id, **kwargs):
    cur = get_cursor()
    fields = []
    values = []
    for k, v in kwargs.items():
        fields.append(f"{k} = ?")
        values.append(v)
    values.append(transaction_id)
    sql = f"UPDATE transactions SET {', '.join(fields)} WHERE id = ?"
    cur.execute(sql, values)
    return cur.rowcount


def delete_transaction(transaction_id):
    cur = get_cursor()
    cur.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    return cur.rowcount
