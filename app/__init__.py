from sanic import Sanic
from sanic.exceptions import NotFound
from sanic_openapi import swagger_blueprint

from app.config.dev import DevConfig
from app.core import listener, handler


def register_listeners(app: Sanic):
    app.register_listener(listener.initialize, 'before_server_start')
    app.register_listener(listener.migrate, 'before_server_start')
    app.register_listener(listener.stop, 'before_server_stop')


def register_blueprints(app: Sanic):
    # Add swagger blueprint
    app.blueprint(swagger_blueprint)

    from app.views.api import user
    app.blueprint(user.blueprint)


def register_exceptions(app: Sanic):
    app.error_handler.add(NotFound, handler.not_found)


def create_app() -> Sanic:
    app = Sanic(__name__)

    app.config.from_object(DevConfig)

    register_listeners(app)
    register_blueprints(app)
    register_exceptions(app)

    return app
