

from flask import Flask
from flask_login import LoginManager

from src.test_task.application.config import settings
from src.test_task.application.shared.dependency_injection.interfaces import InterfacesContainer
from src.test_task.application.shared.dependency_injection.services import ServiceContainer

login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["DATABASE_URL"] = settings.DATABASE_DSN
    app.config["WTF_CSRF_ENABLED"] = settings.WTF_CSRF_ENABLED

    login_manager.init_app(app)
    import src.test_task.application.login

    service_container = ServiceContainer()
    service_container.config.db.dsn.from_value(settings.DATABASE_DSN)
    app.service_container = service_container

    interface_container = InterfacesContainer()
    app.interface_container = interface_container

    from src.test_task.interfaces.ssr.endpoints import auth, product, cart, order
    service_container.wire(modules=[auth, product, cart, order])
    interface_container.wire(modules=[auth, product, cart, order])

    from src.test_task.interfaces.ssr.endpoints.auth import auth_bp
    app.register_blueprint(auth_bp)

    from src.test_task.interfaces.ssr.endpoints.product import product_bp
    app.register_blueprint(product_bp)

    from src.test_task.interfaces.ssr.endpoints.cart import cart_bp
    app.register_blueprint(cart_bp)

    from src.test_task.interfaces.ssr.endpoints.order import order_bp
    app.register_blueprint(order_bp)

    from src.test_task.interfaces.ssr.endpoints.index import bp
    app.register_blueprint(bp)
    return app