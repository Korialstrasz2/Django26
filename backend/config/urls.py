from django.contrib import admin
from django.urls import path
from django.http import JsonResponse
from core.api import api


def root(request):
    return JsonResponse({'status': 'ok', 'service': 'lan-game-backend'})


urlpatterns = [
    path('', root),
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]
