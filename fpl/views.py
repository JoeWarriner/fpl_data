from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponse
from pathlib import Path
import os


class Home(View):

    def get(self, request):
        with open(Path(os.getcwd(), 'README.md')) as file:
            context = {'markdown_lines': file.readlines() }
            return render(request, 'fpl/home.html', context)

