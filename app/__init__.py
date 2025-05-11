import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# Initialize extensions

db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    ma.init_app(app)

    # Register blueprints here
    from app.routes.bank_statements import bank_statements_bp
    from app.routes.transactions import transactions_bp

    app.register_blueprint(bank_statements_bp)
    app.register_blueprint(transactions_bp)

    return app
