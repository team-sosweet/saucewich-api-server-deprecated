from typing import Type, Dict, Any, List

from app.repositories.connections import DBConnection


class FriendRequestRepository:
    table_creation_query = """
            CREATE TABLE IF NOT EXISTS friend_requests (
                seq int(11) PRIMARY KEY NOT NULL,
                sender int(11) NOT NULL,
                recipient int(11) NOT NULL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                
                FOREIGN KEY (sender) REFERENCES users(seq),
                FOREIGN KEY (recipient) REFERENCES users(seq),
                
                UNIQUE KEY `sender_recipient_id` (sender, recipient)
            ) CHARACTER SET utf8mb4;
    """

    def __init__(self, connection: Type[DBConnection]):
        self.connection = connection

    async def get_all(self, recipient: int) -> List[Dict[str, Any]]:
        query = "SELECT seq, sender, created_at FROM `friends` WHERE recipient = %s;"
        return await self.connection.fetchall(
            query,
            recipient,
        )

    async def save(self, friend_request: Dict[str, int]):
        query = """INSERT INTO `friend_requests` (
            sender,
            recipient
        ) VALUES (%s, %s);"""

        await self.connection.execute(
            query,
            (
                friend_request['sender'],
                friend_request['recipient'],
            ),
        )

    async def delete(self, seq: int):
        query = "DELETE FROM `friend_requests` WHERE seq = %s;"

        await self.connection.execute(
            query,
            seq,
        )
