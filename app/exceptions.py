from sanic.response import text


async def not_found(request, exception):
    return text('not_found', status=404)