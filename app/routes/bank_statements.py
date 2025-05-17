from flask import Blueprint, request, jsonify, g

from app.dao.bank_statement_dao import (
    delete_bank_statement,
    get_bank_statement,
    list_bank_statements,
)
from app.dao.shared import process_bank_statement


bank_statements_bp = Blueprint(
    "bank_statements", __name__, url_prefix="/api/bank-statements"
)


@bank_statements_bp.route("/upload", methods=["POST"])
def upload_bank_statement():
    # Support multiple file uploads
    files = request.files.getlist("file")
    if not files or files == [None]:
        return jsonify({"error": "No file(s) uploaded"}), 400
    db = g.get("db")
    if not db:
        return jsonify({"error": "Database connection error"}), 500

    creation = [process_bank_statement(file) for file in files]
    return jsonify(creation), 201


@bank_statements_bp.route("", methods=["GET"])
def list_bs():
    account_number = request.args.get("account_number")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))
    sort = request.args.getlist("sort")

    return jsonify(
        list_bank_statements(
            account_number=account_number,
            limit=limit,
            offset=offset,
            date_from=date_from,
            date_to=date_to,
            sort=sort,
        )
    )


@bank_statements_bp.route("/<int:id>", methods=["GET"])
def get_bs(id):
    return jsonify(get_bank_statement(id))


@bank_statements_bp.route("/<int:id>", methods=["DELETE"])
def delete_bs(id):
    return jsonify(delete_bank_statement(id)), 204
