from datetime import datetime
from typing import Type, Dict, Any, List, Optional

from werkzeug.security import generate_password_hash

from app.repositories.connections import DBConnection


class UserRepository:
    patchable_fields = [
        'nickname',
        'exp',
        'point',
        'money',
        'kill_stats',
        'death_stats',
        'win_stats',
        'defeat_stats',
        'playtime',
    ]

    table_creation_query = """
            CREATE TABLE IF NOT EXISTS users (
                seq INT(11) AUTO_INCREMENT PRIMARY KEY,
                user_id INT(11) NOT NULL,
                nickname VARCHAR(20) NOT NULL,
                exp     BIGINT  DEFAULT 0,
                point   BIGINT  DEFAULT 0,
                money   BIGINT  DEFAULT 0,
                kill_stats    BIGINT  DEFAULT 0,
                death_stats   BIGINT  DEFAULT 0,
                win_stats     BIGINT  DEFAULT 0,
                defeat_stats  BIGINT  DEFAULT 0,
                playtime BIGINT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                
                FOREIGN KEY (user_id) REFERENCES account(seq)
            ) CHARACTER SET utf8mb4;
    """

    def __init__(self, connection: Type[DBConnection]):
        self.connection = connection

    async def get(self, username: str) -> Optional[Dict[str, Any]]:
        query = "SELECT `users`.*, `account`.`username` FROM `users` LEFT JOIN `account` ON `users`.`user_id` = `account`.`seq` AND `account`.`username` = %s"
        return await self.connection.fetchone(
            query,
            username,
        )

    async def get_all(self) -> List[Dict[str, Any]]:
        query = "SELECT * FROM `users`;"
        return await self.connection.fetchall(
            query,
        )

    async def patch(self, username: str, patch_data: Dict[str, Any]) -> bool:
        if not self._check_patchable_fields(patch_data.keys()):
            raise Exception(
                "fields included patchable field, please check that\n"
                + str(patch_data)
            )

        # FIXME: INNER JOIN is right?
        query = f"""UPDATE `users` INNER JOIN `account` ON `account`.`seq` = `users`.`uesr_id` SET updated_at = %s, {
        ",".join([f'{field} = {value}' for field, value in patch_data.items()])
        } WHERE `account`.`username` = %s;"""

        await self.connection.execute(
            query,
            (
                datetime.now(),
                username,
            ),
        )

        return True

    def _check_patchable_fields(self, fields: List[str]):
        for field in fields:
            if not self._is_patchable_field(field):
                return False
        return True

    def _is_patchable_field(self, field: str) -> bool:
        """
        check it's available field name
        :return: boolean value
        """

        return field in self.patchable_fields

    async def save(self, user: Dict[str, Any]):
        query = """INSERT INTO `users` (
            username,
            password,
            nickname
        ) VALUES (%s, %s, %s);"""

        await self.connection.execute(
            query,
            (
                user['username'],
                generate_password_hash(user['password']),
                user['nickname'],
            ),
        )
