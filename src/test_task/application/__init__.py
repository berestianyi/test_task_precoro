from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["DATABASE_URL"] = settings.DATABASE_DSN
    app.config["WTF_CSRF_ENABLED"] = settings.WTF_CSRF_ENABLED

    return app
