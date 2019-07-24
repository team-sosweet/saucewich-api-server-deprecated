from sanic import Blueprint

from app.views.api.user.information import UserInformationView
from app.views.api.user.money import UserMoneyView
from app.views.api.user.point import UserPointView
from app.views.api.user.signup import UserSignupView

blueprint = Blueprint('user-api', '/user')

blueprint.add_route(UserSignupView.as_view(), '/signup')

blueprint.add_route(UserInformationView.as_view(), '/<username>')
blueprint.add_route(UserMoneyView.as_view(), '/<username>/money')
blueprint.add_route(UserPointView.as_view(), '/<username>/point')
