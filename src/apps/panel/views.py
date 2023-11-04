import logging

from django.core.handlers.wsgi import WSGIRequest
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import TemplateView, ListView

from apps.panel.email_storage import EmailRedisRepository
from apps.panel.mixins import EmailCreateListMixin, ArticleParseListMixin, \
    PanelCommonMixin, PanelStateMixin, AddWomanFormMixin
from apps.panel.models import Article
from apps.panel.tasks import TaskSingletonRedisRepository
from apps.parser.features.get_elemens import StateStorageRepository

lg = logging.getLogger(__name__)


class PanelView(
    EmailCreateListMixin,
    ArticleParseListMixin,
    PanelStateMixin,
    PanelCommonMixin,
    AddWomanFormMixin,
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
@require_POST
def clear_emails(request: WSGIRequest) -> HttpResponse:
    email_storage = EmailRedisRepository()
    email_storage.clear_emails()
    return HttpResponse()


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


@csrf_exempt
@require_POST
def make_photo():
    pass
