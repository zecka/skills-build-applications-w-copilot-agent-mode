from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    universe = models.CharField(max_length=50)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class FitUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    hero_alias = models.CharField(max_length=120)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='users')

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name


class Activity(models.Model):
    user = models.ForeignKey(FitUser, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=120)
    duration_minutes = models.PositiveIntegerField()
    calories_burned = models.PositiveIntegerField()
    activity_date = models.DateField()

    class Meta:
        db_table = 'activities'

    def __str__(self):
        return f"{self.activity_type} ({self.user.name})"


class LeaderboardEntry(models.Model):
    user = models.OneToOneField(FitUser, on_delete=models.CASCADE, related_name='leaderboard_entry')
    points = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']

    def __str__(self):
        return f"{self.user.name} - rank {self.rank}"


class Workout(models.Model):
    user = models.ForeignKey(FitUser, on_delete=models.CASCADE, related_name='workouts')
    title = models.CharField(max_length=150)
    focus_area = models.CharField(max_length=120)
    difficulty = models.CharField(max_length=30)
    recommended_duration = models.PositiveIntegerField()

    class Meta:
        db_table = 'workouts'

    def __str__(self):
        return f"{self.title} ({self.user.name})"
