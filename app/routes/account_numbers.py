from flask import Blueprint, request, jsonify

from app.dao.bank_statement_dao import get_unique_account_numbers


account_numbers_bp = Blueprint(
    "account_numbers", __name__, url_prefix="/api/account-numbers"
)


@account_numbers_bp.route("", methods=["GET"])
def list_account_numbers():
    """
    Get unique account numbers with pagination and search functionality.

    Query parameters:
    - q: Optional search term to filter account numbers
    - limit: Number of records to return (default: 10)
    - offset: Number of records to skip (default: 0)
    - sort: Sort parameters (can be used multiple times)
    """
    q = request.args.get("q")
    limit = int(request.args.get("limit", 10))
    offset = int(request.args.get("offset", 0))
    sort = request.args.getlist("sort")

    return jsonify(
        get_unique_account_numbers(
            q=q,
            limit=limit,
            offset=offset,
            sort=sort,
        )
    )
