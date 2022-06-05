from turtle import position
from django.shortcuts import render
from django.http import HttpResponse
from predictor.models import Player

def top(request):
    context = {
        'positions':{} 
    }
    context['positions']['Strikers'] = list(Player.objects.filter(position='FWD')[:3])
    context['positions']['Midfielders'] = list(Player.objects.filter(position='MID')[:3])
    context['positions']['Defenders'] = list(Player.objects.filter(position='DEF')[:3])
    context['positions']['Goalkeepers'] = list(Player.objects.filter(position='GK')[:3])

    return render(request, 'predictor/topplayers.html', context)




