from django.contrib import admin

from .models import Activity, FitUser, LeaderboardEntry, Team, Workout


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'universe')
    search_fields = ('name', 'universe')


@admin.register(FitUser)
class FitUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'hero_alias', 'team')
    search_fields = ('name', 'email', 'hero_alias')
    list_filter = ('team',)


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'duration_minutes', 'calories_burned', 'activity_date')
    search_fields = ('user__name', 'activity_type')
    list_filter = ('activity_type', 'activity_date')


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ('user', 'points', 'rank')
    search_fields = ('user__name',)
    list_filter = ('rank',)


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'focus_area', 'difficulty', 'recommended_duration')
    search_fields = ('user__name', 'title', 'focus_area', 'difficulty')
    list_filter = ('focus_area', 'difficulty')
