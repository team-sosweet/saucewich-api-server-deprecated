from sanic import Sanic
from sanic.exceptions import NotFound
from sanic.response import json, text
from sanic_openapi import swagger_blueprint

from app import listeners, exceptions
from app.config.dev import DevConfig
from app.models import db
from app.models.user import User

def register_listeners(app: Sanic):
    app.register_listener(listeners.setup, 'before_server_start')
    app.register_listener(listeners.stop, 'before_server_stop')


def register_blueprints(app: Sanic):
    # Add swagger blueprint
    app.blueprint(swagger_blueprint)

    from app.views.api import user
    app.blueprint(user.blueprint)


def register_exceptions(app: Sanic):
    app.error_handler.add(NotFound, exceptions.not_found)


def create_app() -> Sanic:
    app = Sanic(__name__)

    app.config.from_object(DevConfig)

    register_listeners(app)
    register_blueprints(app)
    register_exceptions(app)

    return app