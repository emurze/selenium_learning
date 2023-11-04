from django.urls import path

from apps.panel.views import (
    PanelView,
    get_state,
    DownloadArticleList,
    clear_emails, MyPanelView, DownloadMyArticleList,
)

urlpatterns = [
    path('', PanelView.as_view(), name='panel'),
    path('state/', get_state, name='state'),
    path('clear_emails/', clear_emails, name='clear_emails'),
    path('download_articles/',
         DownloadArticleList.as_view(),
         name='download_articles'),
    path('women/', MyPanelView.as_view(), name='my_panel'),
    path('my_download_articles/',
         DownloadMyArticleList.as_view(),
         name='my_download_articles')
]
