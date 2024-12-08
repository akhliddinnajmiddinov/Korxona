from django.urls import path
from .views import GetListView

urlpatterns = [
    path('', GetListView),
]