from sanic import Blueprint

from app.views.api.v2.user import (
    field,
    information
)

blueprint = Blueprint.group(
    *field.create_gettable_blueprints(),
    information.blueprint,
    url_prefix='/user/<username>'
)
