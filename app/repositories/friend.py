from typing import Type, Dict, Any, List

from app.repositories.connections import DBConnection


class FriendRepository:
    table_creation_query = """
            CREATE TABLE IF NOT EXISTS friends (
                seq int(11) AUTO_INCREMENT PRIMARY KEY,
                
                user_id int(11) NOT NULL,
                friend_id int(11) NOT NULL,
                
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

                FOREIGN KEY (user_id) REFERENCES users(seq),
                FOREIGN KEY (friend_id) REFERENCES users(seq),
                
                UNIQUE KEY `user_friend_id` (user_id, friend_id)
            ) CHARACTER SET utf8mb4;
    """

    def __init__(self, connection: Type[DBConnection]):
        self.connection = connection

    async def get_all(self, user_id: int) -> List[Dict[str, Any]]:
        query = "SELECT friend_at, created_at FROM `friends` where user_id = %d"
        return await self.connection.fetchall(
            query,
            user_id,
        )

    async def save(self, friend: Dict[str, int]):
        query = """INSERT INTO `friends` (
            user_id,
            friend_id,
        ) VALUES (%d, %d), (%d, %d);"""

        await self.connection.execute(
            query,
            (
                friend['user_id'],
                friend['friend_id'],
                friend['friend_id'],
                friend['user_id'],
            ),
        )
