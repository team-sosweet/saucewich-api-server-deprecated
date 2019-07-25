from sanic import Blueprint

from app.views.api import v1

blueprint = Blueprint.group(
    v1.blueprint,
    url_prefix='/api',
)
