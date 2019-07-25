from sanic import Blueprint

from app.views.api.v1.user import patch, friend_request
from app.views.api.v1.user.friend import UserFriendsView
from app.views.api.v1.user.information import UserInformationView

blueprint = Blueprint.group(
    friend.blueprint,
    friend_request.blueprint,
    information.blueprint,
    *patch.create_patchable_blueprints(),
    url_prefix='/user/<username>'
)
