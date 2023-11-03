from django.urls import path

from apps.panel.views import PanelView, get_state, DownloadArticleList

urlpatterns = [
    path('', PanelView.as_view(), name='panel'),
    path('state/', get_state, name='state'),
    path('download_articles/',
         DownloadArticleList.as_view(),
         name='download_articles')
]
