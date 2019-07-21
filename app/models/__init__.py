from aiopeewee import AioMySQLDatabase, AioModel
from peewee import DoesNotExist
from sanic.exceptions import abort

db = AioMySQLDatabase(
    'saucewich',
    user='root',
    password='',
    host='localhost',
    port=3306
)


class BaseModel(AioModel):
    class Meta:
        database = db

    @classmethod
    async def get_or_none(cls, *query, **filters):
        try:
            return await cls.get(*query, **filters)
        except DoesNotExist:
            pass

    @classmethod
    async def get_by_id(cls, pk):
        return await cls.get(cls._meta.primary_key == pk)

    @classmethod
    async def get_or_404(cls, *query, **filters):
        try:
            return await cls.get(*query, **filters)
        except DoesNotExist:
            abort(404)
