from sanic import Sanic
from sanic.response import json
from sanic_openapi import swagger_blueprint

from app import listeners
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


def create_app() -> Sanic:
    app = Sanic(__name__)

    app.config.from_object(DevConfig)

    register_listeners(app)
    register_blueprints(app)

    @app.get('/test')
    def root(request):
        return json({'2':2})
    return app
