from django.urls import path
from . import views

urlpatterns = [
    path('topplayers', views.top, name = 'topplayers')
]
