from sanic.log import logger

from app.repositories.connections import MySQLConnection, RedisConnection
from app.repositories.friend import FriendRepository
from app.repositories.friend_request import FriendRequestRepository
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

    await RedisConnection.initialize({
        "minsize": 5,
        "maxsize": 10,
    })

    logger.info('Database initialization is completed.')


async def migrate(app, loop):
    await MySQLConnection.execute(UserRepository.table_creation_query)
    await MySQLConnection.execute(FriendRepository.table_creation_query)
    await MySQLConnection.execute(FriendRequestRepository.table_creation_query)

    logger.info('Database migration is completed.')


async def stop(app, loop):
    await MySQLConnection.destroy()
    await RedisConnection.destroy()

    logger.info('Database connection closed.')
