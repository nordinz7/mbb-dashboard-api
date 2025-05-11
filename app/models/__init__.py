from app import db
from datetime import datetime


class BankStatement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    transactions = db.relationship(
        "Transaction", backref="bank_statement", cascade="all, delete-orphan", lazy=True
    )


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank_statement_id = db.Column(
        db.Integer, db.ForeignKey("bank_statement.id"), nullable=False
    )
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(512), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
