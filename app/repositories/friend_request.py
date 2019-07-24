from typing import Type, Dict, Any, List

from app.repositories.connections import DBConnection


class FriendRequestRepository:
    table_creation_query = """
            CREATE TABLE IF NOT EXISTS friend_requests (
                seq int(11) PRIMARY KEY NOT NULL,
                sender int(11) NOT NULL,
                recipient int(11) NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                
                PRIMARY KEY (sender, recipient),
                FOREIGN KEY (sender) REFERENCES users(seq),
                FOREIGN KEY (recipient) REFERENCES users(seq)
            ) CHARACTER SET utf8mb4;
    """

    def __init__(self, connection: Type[DBConnection]):
        self.connection = connection

    async def get_all(self, recipient: int) -> List[Dict[str, Any]]:
        query = "SELECT seq, sender, created_at FROM `friends` WHERE recipient = %d;"
        return await self.connection.fetchall(
            query,
            recipient,
        )

    async def save(self, sender: int, recipient: int):
        query = """INSERT INTO `friend_requests` (
            sender,
            recipient
        ) VALUES (%s, %s);"""

        await self.connection.execute(
            query,
            (
                sender,
                recipient,
            ),
        )

    async def delete(self, seq: int):
        query = "DELETE FROM `friend_requests` WHERE seq = %d;"

        await self.connection.execute(
            query,
            seq,
        )