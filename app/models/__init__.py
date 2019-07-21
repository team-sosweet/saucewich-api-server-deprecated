from aiopeewee import AioMySQLDatabase, AioModel

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
