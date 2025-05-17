from maybankpdf2json import MaybankPdf2Json
from datetime import datetime
from app.dao.bank_statement_dao import create_bank_statement, get_bank_statement
from app.dao.transaction_dao import create_transaction
from app.utils.db import get_db
from app.utils.helper import strip_account_number


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
