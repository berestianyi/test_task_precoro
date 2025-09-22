from flask import Flask
from flask_login import LoginManager

from src.test_task.application.config import settings
from src.test_task.application.shared.dependency_injection.interfaces import InterfacesContainer
from src.test_task.application.shared.dependency_injection.services import ServiceContainer


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["DATABASE_URL"] = settings.DATABASE_DSN
    app.config["WTF_CSRF_ENABLED"] = settings.WTF_CSRF_ENABLED

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"


    service_container = ServiceContainer()
    service_container.config.db.dsn.from_value(settings.DATABASE_DSN)
    app.service_container = service_container

    interface_container = InterfacesContainer()
    app.interface_container = interface_container

    from src.test_task.interfaces.ssr.endpoints import auth
    service_container.wire(modules=[auth])
    interface_container.wire(modules=[auth])

    from src.test_task.interfaces.ssr.endpoints.auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
