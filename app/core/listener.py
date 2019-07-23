from app.models import db, BaseModel


async def setup(app, loop):
    await db.connect(loop)
    await db.create_tables(BaseModel.__subclasses__(), safe=True)


async def stop(app, loop):
    await db.close()
