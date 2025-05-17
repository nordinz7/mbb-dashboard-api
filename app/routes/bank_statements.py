from flask import Blueprint, request, jsonify, send_file
from app import db
from app.models import BankStatement, Transaction
from app.schemas import BankStatementSchema
from sqlalchemy import desc
from datetime import datetime
import io
from maybankpdf2json import MaybankPdf2Json

bank_statements_bp = Blueprint(
    "bank_statements", __name__, url_prefix="/api/bank-statements"
)


@bank_statements_bp.route("/upload", methods=["POST"])
def upload_bank_statement():
    # Support multiple file uploads
    files = request.files.getlist("file")
    if not files or files == [None]:
        return jsonify({"error": "No file(s) uploaded"}), 400
    created_statements = []
    for file in files:
        if not file:
            continue
        filename = file.filename
        mbb = MaybankPdf2Json(file, "04Nov1997")
        data = mbb.json()
        print(data)
        bank_statement = BankStatement(filename=filename)
        db.session.add(bank_statement)
        created_statements.append(bank_statement)
    db.session.commit()
    return BankStatementSchema(many=True).jsonify(created_statements), 201


@bank_statements_bp.route("", methods=["GET"])
def list_bank_statements():
    q = request.args.get("q")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))
    sort = request.args.getlist("sort")
    query = BankStatement.query
    if q:
        query = query.filter(BankStatement.filename.ilike(f"%{q}%"))
    if date_from:
        query = query.filter(BankStatement.created_at >= date_from)
    if date_to:
        query = query.filter(BankStatement.created_at <= date_to)
    for s in sort:
        if s.startswith("-"):
            field = s[1:]
            query = query.order_by(desc(getattr(BankStatement, field, "created_at")))
        else:
            query = query.order_by(getattr(BankStatement, s, "created_at"))
    items = query.offset(offset).limit(limit).all()
    return jsonify(BankStatementSchema(many=True).dump(items))


@bank_statements_bp.route("/<int:id>", methods=["GET"])
def get_bank_statement(id):
    download = request.args.get("download") == "true"
    bank_statement = BankStatement.query.get_or_404(id)
    if download:
        # Placeholder: generate PDF
        pdf_bytes = io.BytesIO(b"PDF content for bank statement")
        return send_file(
            pdf_bytes,
            as_attachment=True,
            download_name=f"{bank_statement.filename}.pdf",
            mimetype="application/pdf",
        )
    return BankStatementSchema().jsonify(bank_statement)


@bank_statements_bp.route("/<int:id>", methods=["DELETE"])
def delete_bank_statement(id):
    bank_statement = BankStatement.query.get_or_404(id)
    db.session.delete(bank_statement)
    db.session.commit()
    return "", 204
