from turtle import position
from django.shortcuts import render
from django.views import View
from django.views.generic.edit import FormView
from django.urls import URLPattern
from django.shortcuts import redirect



from apps.predictor.models import Player
from apps.predictor.forms import PositionSelecter



class TopPlayers(FormView):
    template_name = 'predictor/positionselect.html'
    form_class = PositionSelecter

    def form_valid(self, form):

        position = form.data.get('position')
        context = {
            'positions':{} 
        }
        context['positions'][position] = list(Player.objects.filter(position=position).order_by('-expected_points')[:10])

        return render(None,'predictor/topplayers.html', context)



class TopPlayersAllPositions(View):

    def get(self, request):
        context = {
            'positions':{} 
        }
        for position in ['FWD','MID','DEF','GK']: 
            context['positions'][position] = list(Player.objects.filter(position=position).order_by('-expected_points')[:10])
        return render(request, 'predictor/topplayers.html', context)
    



