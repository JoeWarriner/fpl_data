from turtle import position
from django.shortcuts import render
from django.views import View

from apps.predictor.models import Player


class TopPlayers(View):

    def get(self, request):
        context = {
            'positions':{} 
        }
        for position in ['FWD','MID','DEF','GK']: 
            context['positions'][position] = list(Player.objects.filter(position=position).order_by('-expected_points')[:10])

        return render(request, 'predictor/topplayers.html', context)





