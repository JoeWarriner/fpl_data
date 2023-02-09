from turtle import position
from django.shortcuts import render
from django.http import HttpResponse
from predictor.models import Player
from predictor.regression_predictor import generate_predictions

def top(request):
    context = {
        'positions':{} 
    }
    context['positions']['Strikers'] = list(Player.objects.filter(position='FWD').order_by('expected_points')[:3])
    context['positions']['Midfielders'] = list(Player.objects.filter(position='MID').order_by('expected_points')[:3])
    context['positions']['Defenders'] = list(Player.objects.filter(position='DEF').order_by('expected_points')[:3])
    context['positions']['Goalkeepers'] = list(Player.objects.filter(position='GK').order_by('expected_points')[:3])

    return render(request, 'predictor/topplayers.html', context)


def testing(request):
    generate_predictions()
    return HttpResponse('Request received')




