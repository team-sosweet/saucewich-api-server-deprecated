from sanic import Blueprint

from app.views.api.v1 import user, signup, signin

blueprint = Blueprint.group(
    url_prefix='/v1',
)
