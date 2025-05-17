import glob
import os
import sqlite3
from flask import g

from config import Config

SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "../schemas/")


def get_cursor():
    return g.get("db").cursor()


def get_db_connection():
    conn = sqlite3.connect(Config.DB_FILE_PATH)
    conn.row_factory = sqlite3.Row
    # Initialize all schemas in the schemas directory
    schema_files = sorted(glob.glob(os.path.join(SCHEMA_DIR, "*.sql")))
    for schema_file in schema_files:
        with open(schema_file) as f:
            conn.executescript(f.read())
    return conn


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


# --- Bank Statements CRUD ---
def create_bank_statement(filename, created_at=None):
    cur = get_cursor()
    cur.execute(
        """
        INSERT INTO bank_statements (filename, created_at)
        VALUES (?, COALESCE(?, CURRENT_TIMESTAMP))
        """,
        (filename, created_at),
    )
    return cur.lastrowid


def get_bank_statement(bank_statement_id):
    cur = get_cursor()
    cur.execute("SELECT * FROM bank_statements WHERE id = ?", (bank_statement_id,))
    row = cur.fetchone()
    return dict(row) if row else None


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
