from turtle import position
from django.shortcuts import render
from django.views import View
from predictor.models import Player
from predictor.prediction_models.regression_predictor import generate_predictions
from predictor.basic_predictor import get_latest_predictions


class TopPlayers(View):

    def get(self, request):
        get_latest_predictions()
        context = {
            'positions':{} 
        }
        for position in ['FWD','MID','DEF','GK']: 
            context['positions'][position] = list(Player.objects.filter(position=position).order_by('-expected_points')[:10])

        return render(request, 'predictor/topplayers.html', context)





