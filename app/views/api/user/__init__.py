from sanic import Blueprint

from app.views.api.user.information import UserInformationView
from app.views.api.user.patch import UserPatchView
from app.views.api.user.signup import UserSignupView

blueprint = Blueprint('user-api', '/user')

blueprint.add_route(UserSignupView.as_view(), '/signup')

blueprint.add_route(UserInformationView.as_view(), '/<username>')
blueprint.add_route(UserPatchView.as_view(), '/<username>/<field_name>')
