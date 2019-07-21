from peewee import CharField, IntegerField, BigIntegerField

from app.models import BaseModel


class User(BaseModel):
    username = CharField(max_length=10)
    password = CharField(max_length=10)
    nickname = CharField(max_length=10)

    exp = IntegerField(default=0)
    point = IntegerField(default=0)
    money = IntegerField(default=0)

    # KDR
    kill = IntegerField(default=0)
    death = IntegerField(default=0)

    # W/L
    wins = IntegerField(default=0)
    defeats = IntegerField(default=0)

    # The unit is in seconds.
    playtime = BigIntegerField(default=0)
