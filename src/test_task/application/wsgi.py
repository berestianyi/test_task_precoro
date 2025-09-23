from src.test_task.application import create_app
from src.test_task.application.middleware import init_cookie_middleware

app = create_app()
init_cookie_middleware(app)