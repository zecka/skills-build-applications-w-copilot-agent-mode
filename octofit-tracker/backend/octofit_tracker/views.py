from rest_framework import viewsets

from .models import Activity, FitUser, LeaderboardEntry, Team, Workout
from .serializers import (
    ActivitySerializer,
    FitUserSerializer,
    LeaderboardEntrySerializer,
    TeamSerializer,
    WorkoutSerializer,
)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by('name')
    serializer_class = TeamSerializer


class FitUserViewSet(viewsets.ModelViewSet):
    queryset = FitUser.objects.select_related('team').all().order_by('name')
    serializer_class = FitUserSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.select_related('user').all().order_by('-activity_date')
    serializer_class = ActivitySerializer


class LeaderboardEntryViewSet(viewsets.ModelViewSet):
    queryset = LeaderboardEntry.objects.select_related('user').all()
    serializer_class = LeaderboardEntrySerializer


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.select_related('user').all().order_by('title')
    serializer_class = WorkoutSerializer
