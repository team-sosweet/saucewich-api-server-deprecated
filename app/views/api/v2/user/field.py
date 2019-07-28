from typing import List, Type

from sanic import Blueprint
from sanic.exceptions import abort
from sanic.response import json
from sanic.views import HTTPMethodView
from sanic_openapi import doc

from app.repositories.connections import MySQLConnection
from app.repositories.user import UserRepository
from app.services.user import UserService


def create_gettable_blueprint(patch_field: str, patch_field_type: Type[type]) -> Blueprint:
    blueprint = Blueprint(f'user-patch-{patch_field}-api', url_prefix=f'/{patch_field}')

    class UserFieldGetterView(HTTPMethodView):
        repository = UserRepository(MySQLConnection)
        service = UserService(repository)

        field_name: str = patch_field
        field_type: type = patch_field_type

        @doc.summary(f'Get {field_name} of user')
        @doc.produces(
            {
                patch_field: patch_field_type
            },
            content_type='application/json',
            description=f'The value of {patch_field} field'
        )
        async def get(self, request, username: str):
            field_name = self.field_name
            if field_name not in self.repository.patchable_fields:
                abort(404)
            user = await self.service.get(username)
            return json({
                field_name: user[field_name]
            })

    blueprint.add_route(UserFieldGetterView.as_view(), '/')

    return blueprint


def create_gettable_blueprints() -> List[Blueprint]:
    def filter_nickname(s: str):
        if s == 'nickname':
            return s, str
        else:
            return s, int

    fields_with_type = map(filter_nickname, UserRepository.patchable_fields)
    return list(
        map(lambda args: create_gettable_blueprint(*args), fields_with_type)
    )
