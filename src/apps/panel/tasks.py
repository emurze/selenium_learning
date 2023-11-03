import logging

import django
import redis
from celery import shared_task
from django.db import transaction

from apps.panel.models import Article
from apps.parser.container import ParserApp
from apps.parser.features.get_elemens import StateStorageRepository
from config.settings.redis import (
    REDIS_FEATURE_DB,
    REDIS_FEATURE_PORT,
    REDIS_FEATURE_HOST,
)

lg = logging.getLogger(__name__)


class TaskSingletonRedisRepository:
    def __init__(self) -> None:
        self.conn = redis.Redis(
            db=REDIS_FEATURE_DB,
            port=REDIS_FEATURE_PORT,
            host=REDIS_FEATURE_HOST,
        )

    def is_exists(self, name: str) -> bool:
        return bool(self.conn.get(name))

    def set_task(self, name: str) -> None:
        self.conn.set(name, 'True')

    def remove_task(self, name: str) -> None:
        self.conn.delete(name)


@shared_task
def request_articles() -> None:
    singleton = TaskSingletonRedisRepository()
    if not singleton.is_exists('request_articles'):
        singleton.set_task('request_articles')

        parser = ParserApp()
        result = parser.parse()

        for item in result['articles']:
            try:
                Article.objects.create(
                    title=item['name'],
                    href=item['href'],
                    src=item['image'],
                )
            except django.db.utils.IntegrityError:
                pass

        singleton.remove_task('request_articles')
