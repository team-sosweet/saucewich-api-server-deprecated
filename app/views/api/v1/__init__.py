from sanic import Blueprint

from app.views.api.v1 import user

blueprint = Blueprint.group(
    user.blueprint,
    url_prefix='/v1',
)
