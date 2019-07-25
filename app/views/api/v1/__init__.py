from sanic import Blueprint

from app.views.api.v1 import user, signup

blueprint = Blueprint.group(
    user.blueprint,
    signup.blueprint,
    url_prefix='/v1',
)
