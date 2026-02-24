from rest_framework import serializers

from .models import Activity, FitUser, LeaderboardEntry, Team, Workout


class ObjectIdStringModelSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return str(obj.pk)


class TeamSerializer(ObjectIdStringModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'universe']


class FitUserSerializer(ObjectIdStringModelSerializer):
    team = serializers.CharField(source='team_id', read_only=True)
    team_id = serializers.PrimaryKeyRelatedField(queryset=Team.objects.all(), source='team', write_only=True)

    class Meta:
        model = FitUser
        fields = ['id', 'name', 'email', 'hero_alias', 'team', 'team_id']


class ActivitySerializer(ObjectIdStringModelSerializer):
    user = serializers.CharField(source='user_id', read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=FitUser.objects.all(), source='user', write_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'user', 'user_id', 'activity_type', 'duration_minutes', 'calories_burned', 'activity_date']


class LeaderboardEntrySerializer(ObjectIdStringModelSerializer):
    user = serializers.CharField(source='user_id', read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=FitUser.objects.all(), source='user', write_only=True)

    class Meta:
        model = LeaderboardEntry
        fields = ['id', 'user', 'user_id', 'points', 'rank']


class WorkoutSerializer(ObjectIdStringModelSerializer):
    user = serializers.CharField(source='user_id', read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=FitUser.objects.all(), source='user', write_only=True)

    class Meta:
        model = Workout
        fields = ['id', 'user', 'user_id', 'title', 'focus_area', 'difficulty', 'recommended_duration']
