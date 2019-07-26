from sanic import Blueprint

from app.views.api.v1 import user, signup, signin

blueprint = Blueprint.group(
    user.blueprint,
    signin.blueprint,
    signup.blueprint,
    url_prefix='/v1',
)
