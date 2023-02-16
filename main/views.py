from django.shortcuts import render
from django.views import View
from pathlib import Path
import os


class Home(View):

    def get(self, request):
        return render(request, 'main/home.html')

