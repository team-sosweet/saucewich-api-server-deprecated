from sanic import Blueprint

from app.views.api.v1.user import patch
from app.views.api.v1.user.friend import UserFriendsView
from app.views.api.v1.user.information import UserInformationView
from app.views.api.v1.user.signup import UserSignupView

blueprint = Blueprint.group(
    friend.blueprint,
    information.blueprint,
    *patch.create_patchable_blueprints(),
    url_prefix='/user/<username>'
)
