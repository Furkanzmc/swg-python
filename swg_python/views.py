# Django
from django.shortcuts import render


def render_swagger_view(request):
    return render(request, 'swg_python/index.html', {})
