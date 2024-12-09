from django.urls import path
from .views import GetListView

app_name='main'
urlpatterns = [
    path('', GetListView, name='get_list'),
]