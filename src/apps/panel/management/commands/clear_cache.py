import logging

import redis
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from apps.panel.tasks import TaskSingletonRedisRepository
from apps.parser.features.get_elemens import StateStorageRepository

User = get_user_model()
lg = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'This command creates superuser'

    def handle(self, *_, **__) -> None:
        state_storage = StateStorageRepository()
        singleton_storage = TaskSingletonRedisRepository()

        state_storage.clear_state()
        singleton_storage.remove_task('request_articles')
