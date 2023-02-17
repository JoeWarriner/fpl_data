from django.urls import path
from apps.predictor.views import TopPlayers, TopPlayersAllPositions

app_name = 'predictor'

urlpatterns = [
    path('top-players/all',TopPlayersAllPositions.as_view() ),
    path('top-players', TopPlayers.as_view() )  
]
