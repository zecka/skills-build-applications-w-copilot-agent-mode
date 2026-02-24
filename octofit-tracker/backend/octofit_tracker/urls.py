import os

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .views import (
    ActivityViewSet,
    FitUserViewSet,
    LeaderboardEntryViewSet,
    TeamViewSet,
    WorkoutViewSet,
)

codespace_name = os.environ.get('CODESPACE_NAME')
if codespace_name:
    base_url = f"https://{codespace_name}-8000.app.github.dev"
else:
    base_url = "http://localhost:8000"

router = routers.DefaultRouter()
router.register(r'users', FitUserViewSet, basename='users')
router.register(r'teams', TeamViewSet, basename='teams')
router.register(r'activities', ActivityViewSet, basename='activities')
router.register(r'leaderboard', LeaderboardEntryViewSet, basename='leaderboard')
router.register(r'workouts', WorkoutViewSet, basename='workouts')


@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {
            'users': f'{base_url}/api/users/',
            'teams': f'{base_url}/api/teams/',
            'activities': f'{base_url}/api/activities/',
            'leaderboard': f'{base_url}/api/leaderboard/',
            'workouts': f'{base_url}/api/workouts/',
        }
    )

urlpatterns = [
    path('', api_root, name='root'),
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
]
