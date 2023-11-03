import logging

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.views.generic import TemplateView, ListView

from apps.panel.mixins import EmailCreateListMixin, ArticleParseListMixin, \
    PanelCommonMixin, PanelStateMixin
from apps.panel.models import Article
from apps.panel.tasks import TaskSingletonRedisRepository
from apps.parser.features.get_elemens import StateStorageRepository

lg = logging.getLogger(__name__)


class PanelView(
    EmailCreateListMixin,
    ArticleParseListMixin,
    PanelStateMixin,
    PanelCommonMixin,
    TemplateView,
):
    template_name = 'panel.html'
    success_url = reverse_lazy('panel')


class DownloadArticleList(ListView):
    queryset = Article.objects.only('src', 'href')
    paginate_by = 35
    template_name = 'articles.html'
    context_object_name = 'articles'


@csrf_exempt
@require_GET
def get_state(request: WSGIRequest) -> JsonResponse:
    singleton = TaskSingletonRedisRepository()
    if singleton.is_exists('request_articles'):
        storage = StateStorageRepository()
        state = storage.get_state()
    else:
        state = 'parse'
    return JsonResponse({
        'state': state
    })
