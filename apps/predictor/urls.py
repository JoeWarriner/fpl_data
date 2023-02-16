from django.urls import path
from apps.predictor.views import TopPlayers

app_name = 'predictor'

urlpatterns = [
    path('', TopPlayers.as_view())
]
