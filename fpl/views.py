from django.shortcuts import render
from pathlib import Path
import os

def home(request):

    with open(Path(os.getcwd(), 'README.md')) as file:
        context = {'markdown_lines': file.readlines() }
        return render(request, 'fpl/home.html', context)
    

    