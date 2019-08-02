from sanic import Blueprint

from app.views.api.v2 import user

blueprint = Blueprint.group(
    user.blueprint,
    url_prefix='/v2',
)
