from flask import Flask, g
from flask_marshmallow import Marshmallow
from flask_cors import CORS

from app.utils.db import get_db_connection


ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    CORS(app)  # 👈 Enables CORS for all routes and all origins
    app.config.from_object("config.Config")

    ma.init_app(app)

    # Register blueprints here
    from app.routes.bank_statements import bank_statements_bp
    from app.routes.transactions import transactions_bp

    app.register_blueprint(bank_statements_bp)
    app.register_blueprint(transactions_bp)

    @app.before_request
    def before_request():
        if "db" not in g:
            g.db = get_db_connection()

    @app.teardown_appcontext
    def teardown_db(exception):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @app.route("/")
    def root():
        return {"message": "Ok"}

    return app
