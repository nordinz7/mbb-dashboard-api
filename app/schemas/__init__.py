from app import ma
from app.models import BankStatement, Transaction


class TransactionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Transaction
        load_instance = True
        include_fk = True


class BankStatementSchema(ma.SQLAlchemyAutoSchema):
    transactions = ma.Nested(TransactionSchema, many=True)

    class Meta:
        model = BankStatement
        load_instance = True
