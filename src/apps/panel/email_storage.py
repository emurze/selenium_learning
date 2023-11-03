from collections.abc import Generator

import redis

from config.settings.redis import (
    REDIS_FEATURE_DB,
    REDIS_FEATURE_PORT,
    REDIS_FEATURE_HOST,
    REDIS_EMAIL_STORAGE,
)


class EmailRedisRepository:
    def __init__(self) -> None:
        self.conn = redis.Redis(
            db=REDIS_FEATURE_DB,
            port=REDIS_FEATURE_PORT,
            host=REDIS_FEATURE_HOST,
        )

    def add_email(self, email: str) -> None:
        self.conn.sadd(
            REDIS_EMAIL_STORAGE,
            email
        )

    def get_all_emails(self) -> Generator:
        return (
            email.decode('utf-8')
            for email in self.conn.smembers(REDIS_EMAIL_STORAGE)
        )
