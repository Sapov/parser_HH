from django.urls import path

from .views import search, IndexListView

urlpatterns = [
    path('', search, name='search_form'),
    # path('list/', index_view, name='index_list'),
    path('list/', IndexListView.as_view(), name='index_list'),
]
