from sanic import Blueprint

from app.views.api import v1, v2

blueprint = Blueprint.group(
    v1.blueprint,
    v2.blueprint,
    url_prefix='/api',
)
