import logging

from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import CreateView

from apps.panel.email_storage import EmailRedisRepository
from apps.panel.forms import CreateEmailForm, CreateWomanForm
from apps.panel.models import Article
from utils import mixin_for
from .tasks import request_articles, TaskSingletonRedisRepository
from ..parser.features.get_elemens import StateStorageRepository

lg = logging.getLogger(__name__)


class EmailCreateListMixin(mixin_for(CreateView)):
    def post(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        if (form := CreateEmailForm(request.POST)).is_valid():
            cd = form.cleaned_data
            email = cd['email']
            storage = EmailRedisRepository()
            storage.add_email(email)
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        kwargs['form'] = CreateEmailForm()
        storage = EmailRedisRepository()
        kwargs['emails'] = storage.get_all_emails()
        return super().get_context_data(**kwargs)


class ArticleParseListMixin(mixin_for(CreateView)):
    def post(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        if request.POST.get('parse'):
            request_articles.delay()
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        kwargs['articles'] = Article.objects.only('src', 'href')\
            [:35]
        kwargs['articles_amount'] = Article.objects.count()
        return super().get_context_data(**kwargs)


class PanelCommonMixin(mixin_for(CreateView)):
    def post(self, request: WSGIRequest, *args, **kwargs) -> HttpResponse:
        return redirect(self.success_url)


class PanelStateMixin:
    def get_context_data(self, **kwargs) -> dict:
        singleton = TaskSingletonRedisRepository()
        if singleton.is_exists('request_articles'):
            storage = StateStorageRepository()
            kwargs['state'] = storage.get_state()
        else:
            kwargs['state'] = 'parse'
        return super().get_context_data(**kwargs)


class AddWomanFormMixin:
    def get_context_data(self, **kwargs) -> dict:
        kwargs['woman_form'] = CreateWomanForm()
        return super().get_context_data(**kwargs)
