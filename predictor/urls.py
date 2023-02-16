from django.urls import path
from predictor.views import TopPlayers


urlpatterns = [
    path('', TopPlayers.as_view())
]
