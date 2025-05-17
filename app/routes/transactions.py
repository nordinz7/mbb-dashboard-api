from flask import Blueprint, request, jsonify

from app.dao.transaction_dao import (
    delete_transaction,
    get_transaction,
    list_transactions,
)

transactions_bp = Blueprint("transactions", __name__, url_prefix="/api/transactions")


@transactions_bp.route("", methods=["GET"])
def list_trs():
    q = request.args.get("q")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))
    sort = request.args.getlist("sort")

    return jsonify(
        list_transactions(
            q=q,
            limit=limit,
            offset=offset,
            date_from=date_from,
            date_to=date_to,
            sort=sort,
        )
    )


@transactions_bp.route("/<int:id>", methods=["GET"])
def get_trs(id):
    return jsonify(get_transaction(id))


@transactions_bp.route("/<int:id>", methods=["DELETE"])
def delete_trs(id):
    return jsonify(delete_transaction(id)), 204
