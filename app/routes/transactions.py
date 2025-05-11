from flask import Blueprint, request, jsonify
from app import db
from app.models import Transaction
from app.schemas import TransactionSchema
from sqlalchemy import desc
from datetime import datetime

transactions_bp = Blueprint("transactions", __name__, url_prefix="/api/transactions")


@transactions_bp.route("", methods=["GET"])
def list_transactions():
    q = request.args.get("q")
    bank_statement_id = request.args.get("bank_statement_id")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))
    sort = request.args.getlist("sort")
    query = Transaction.query
    if q:
        query = query.filter(Transaction.description.ilike(f"%{q}%"))
    if bank_statement_id:
        query = query.filter(Transaction.bank_statement_id == bank_statement_id)
    if date_from:
        query = query.filter(Transaction.date >= date_from)
    if date_to:
        query = query.filter(Transaction.date <= date_to)
    for s in sort:
        if s.startswith("-"):
            field = s[1:]
            query = query.order_by(desc(getattr(Transaction, field, "created_at")))
        else:
            query = query.order_by(getattr(Transaction, s, "created_at"))
    items = query.offset(offset).limit(limit).all()
    return jsonify(TransactionSchema(many=True).dump(items))


@transactions_bp.route("/<int:id>", methods=["GET"])
def get_transaction(id):
    transaction = Transaction.query.get_or_404(id)
    return TransactionSchema().jsonify(transaction)
