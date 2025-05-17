from flask import Blueprint, request, jsonify, g
from datetime import datetime
from maybankpdf2json import MaybankPdf2Json

from app.utils.db import create_transaction, list_transactions


bank_statements_bp = Blueprint(
    "bank_statements", __name__, url_prefix="/api/bank-statements"
)


@bank_statements_bp.route("/upload", methods=["POST"])
def upload_bank_statement():
    # Support multiple file uploads
    files = request.files.getlist("file")
    if not files or files == [None]:
        return jsonify({"error": "No file(s) uploaded"}), 400
    for file in files:
        if not file:
            continue
        filename = file.filename
        mbb = MaybankPdf2Json(file, "04Nov1997")
        data = mbb.json()
        print(f"Parsed data: {data}")
        db = g.get("db").cursor()
        print(f"DB: {db}")
        if not db:
            return jsonify({"error": "Database connection error"}), 500
        for transaction in data:
            t_date = datetime.strptime(transaction["date"], "%d/%m/%y").date()
            t_amount = float(transaction["trans"])
            t_description = transaction["desc"]
            t_bal = float(transaction["bal"])
            # Assuming a function create_transaction exists to save the transaction
            r = create_transaction(t_date, t_amount, t_description, t_bal)
            print(f"Transaction created with ID: {r}")
    return jsonify(list_transactions()), 201


@bank_statements_bp.route("", methods=["GET"])
def list_bank_statements():
    q = request.args.get("q")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))
    sort = request.args.getlist("sort")
    # query =
    # if q:
    #     query = query.filter(BankStatement.filename.ilike(f"%{q}%"))
    # if date_from:
    #     query = query.filter(BankStatement.created_at >= date_from)
    # if date_to:
    #     query = query.filter(BankStatement.created_at <= date_to)
    # for s in sort:
    #     if s.startswith("-"):
    #         field = s[1:]
    #         query = query.order_by(desc(getattr(BankStatement, field, "created_at")))
    #     else:
    #         query = query.order_by(getattr(BankStatement, s, "created_at"))
    # items = query.offset(offset).limit(limit).all()
    return jsonify(
        {
            "items": [],  # items,
            "total": 0,  # query.count(),
        }
    )


@bank_statements_bp.route("/<int:id>", methods=["GET"])
def get_bank_statement(id):
    download = request.args.get("download") == "true"
    return jsonify(
        {
            "id": id,
            "filename": "example.pdf",
            "created_at": datetime.now().isoformat(),
            "transactions": [
                {
                    "date": "2023-01-01",
                    "amount": 100.0,
                    "description": "Example transaction",
                }
            ],
        }
    )


@bank_statements_bp.route("/<int:id>", methods=["DELETE"])
def delete_bank_statement(id):
    return "", 204
