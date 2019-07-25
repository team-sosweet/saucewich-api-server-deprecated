from sanic import Blueprint

from app.views.api.v1.user import patch
from app.views.api.v1.user.friend import UserFriendsView
from app.views.api.v1.user.information import UserInformationView
from app.views.api.v1.user.signup import UserSignupView

blueprint = Blueprint('user-api')

# blueprint.add_route(UserSignupView.as_view(), '/signup')

blueprint.add_route(UserInformationView.as_view(), '/')

blueprint = Blueprint.group(blueprint,
                            friend.blueprint,
                            *patch.create_patchable_blueprints(),
                            url_prefix='/user/<username>')
