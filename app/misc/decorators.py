from functools import wraps
from typing import Optional, Dict, Any

from sanic.exceptions import abort
from sanic.request import Request

from app.repositories.connections import RedisConnection


def authorized(original):
    @wraps(original)
    async def decorated(request: Request, *args, **kwargs):
        session_id: Optional[str] = request.cookies.get('session_id')
        if session_id is None:
            abort(403)

        user_data = await RedisConnection.get('auth:' + session_id)
        if user_data is None:
            abort(401)

    return decorated
