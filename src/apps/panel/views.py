import logging

from django.core.handlers.wsgi import WSGIRequest
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.views.generic import TemplateView, ListView

from apps.panel.email_storage import EmailRedisRepository
from apps.panel.mixins import EmailCreateListMixin, ArticleParseListMixin, \
    PanelCommonMixin, PanelStateMixin, AddWomanFormMixin, BasePanelMixin, \
    MyPanelListMixin, AddWomanFileSystemFormMixin, CreateWomanMixin
from apps.panel.models import Article, Woman
from apps.panel.tasks import TaskSingletonRedisRepository
from apps.parser.features.get_elemens import StateStorageRepository

lg = logging.getLogger(__name__)


class PanelView(
    ArticleParseListMixin,
    PanelStateMixin,
    BasePanelMixin,
):
    paginate_by = 30
    success_url = reverse_lazy('panel')
    template_name = 'pages/panel.html'

    def get_context_data(self, **kwargs):
        kwargs['paginate_by'] = self.paginate_by
        return super().get_context_data(**kwargs)


class DownloadArticleList(ListView):
    queryset = Article.objects.all()
    paginate_by = 30
    template_name = 'articles.html'
    context_object_name = 'articles'


class DownloadMyArticleList(ListView):
    queryset = Woman.objects.all()
    paginate_by = 30
    template_name = 'women.html'
    context_object_name = 'women'


class MyPanelView(
    CreateWomanMixin,
    AddWomanFileSystemFormMixin,
    MyPanelListMixin,
    BasePanelMixin,
):
    paginate_by = 30
    success_url = reverse_lazy('my_panel')
    template_name = 'pages/my_panel.html'

    def get_context_data(self, **kwargs):
        kwargs['paginate_by'] = self.paginate_by
        return super().get_context_data(**kwargs)


@csrf_exempt
@require_POST
def clear_emails(request: WSGIRequest) -> HttpResponse:
    email_storage = EmailRedisRepository()
    email_storage.clear_emails()
    return HttpResponse()


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
def make_photo(request: WSGIRequest) -> HttpResponse:
    lg.debug(request.POST)
    return redirect(reverse_lazy('panel'))
