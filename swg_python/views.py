# Django
from django.shortcuts import render
from django.conf import settings

def render_swagger_view(request):
    redoc_enabled = getattr(settings, 'SWG_ENABLE_REDOC', True)
    if redoc_enabled:
        return render(request, 'swg_python/redoc.html', {})

    return render(request, 'swg_python/index.html', {})
