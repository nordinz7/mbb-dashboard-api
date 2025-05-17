import glob
import os
import sqlite3
from flask import g
from maybankpdf2json import MaybankPdf2Json
from datetime import datetime

from app.utils.helper import strip_account_number
from config import Config

SCHEMA_DIR = os.path.join(os.path.dirname(__file__), "../schemas/")


def get_db():
    if "db" not in g:
        g.db = get_db_connection()
    return g.db


def get_cursor():
    return get_db().cursor()


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


def process_bank_statement(file):
    o = {
        "bank_statement_id": None,
        "date": None,
        "account_number": None,
        "success": False,
        "message": None,
        "fileName": None,
    }

    if not file:
        o["message"] = "No file provided"
        return o

    o["fileName"] = file.filename

    mbb = MaybankPdf2Json(file, "04Nov1997")
    data = mbb.jsonV2()

    b_date = datetime.strptime(data["statement_date"], "%d/%m/%y").date()
    b_account_number = strip_account_number(data["account_number"])

    try:
        exist = get_bank_statement(
            date=b_date,
            account_number=b_account_number,
        )

        if exist:
            o["bank_statement_id"] = exist["id"]
            o["date"] = exist["date"]
            o["account_number"] = exist["account_number"]
            o["message"] = "Bank statement already exists"
            return o

        b_id = create_bank_statement(
            date=b_date,
            account_number=b_account_number,
        )

        o["bank_statement_id"] = b_id
        o["date"] = b_date
        o["account_number"] = b_account_number

        for transaction in data["transactions"]:
            t_date = datetime.strptime(transaction["date"], "%d/%m/%y").date()
            t_amount = float(transaction["trans"])
            t_description = transaction["desc"]
            t_bal = float(transaction["bal"])
            t_id = create_transaction(t_date, t_amount, t_description, t_bal, b_id)
            if not t_id:
                o["message"] = "Failed to create transaction"
                return o

        get_db().commit()

        o["success"] = True
        o["message"] = "Bank statement and transactions processed successfully"
    except Exception as e:
        o["message"] = f"Error processing bank statement: {e}"
    return o
