from sanic import Blueprint

from app.views.api.v2.user import (
    field,
    friend,
    friend_request,
    information
)

blueprint = Blueprint.group(
    friend.blueprint,
    friend_request.blueprint,
    information.blueprint,
    *field.create_gettable_blueprints(),
    url_prefix='/user/<username>'
)
