from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from . import models

def index_view(request):
    return render(request, "index.html")
