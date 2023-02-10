from turtle import position
from django.shortcuts import render
from django.http import HttpResponse
from predictor.models import Player
from predictor.prediction_models.regression_predictor import generate_predictions
from predictor.basic_predictor import get_latest_predictions


def top(request):
    get_latest_predictions()
    context = {
        'positions':{} 
    }
    for position in ['FWD','MID','DEF','GK']: 
        context['positions'][position] = list(Player.objects.filter(position=position).order_by('-expected_points')[:10])


    return render(request, 'predictor/topplayers.html', context)





