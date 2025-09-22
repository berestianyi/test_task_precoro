from dependency_injector import containers, providers

from src.test_task.interfaces.ssr.forms.auth import RegisterForm, LoginForm


class InterfacesContainer(containers.DeclarativeContainer):
    register_form = providers.Factory(RegisterForm)
    login_from = providers.Factory(LoginForm)
