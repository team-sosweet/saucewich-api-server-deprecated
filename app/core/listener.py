import os

from sanic.log import logger

from app.repositories.connections import MySQLConnection
from app.repositories.user import UserRepository


async def initialize(app, loop):
    await MySQLConnection.initialize({
        'use_unicode': True,
        'charset': 'utf8mb4',
        'user': 'root',
        'password': '',
        'db': 'saucewich',
        'host': 'localhost',
        'port': 3306,
        'loop': None,
        'autocommit': True,
    })


async def migrate(app, loop):
    await MySQLConnection.execute(UserRepository.table_creation_query)


async def stop(app, loop):
    await MySQLConnection.close()
