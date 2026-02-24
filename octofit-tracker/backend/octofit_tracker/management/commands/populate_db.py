from datetime import date

from django.core.management.base import BaseCommand

from octofit_tracker.models import Activity, FitUser, LeaderboardEntry, Team, Workout


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        LeaderboardEntry.objects.all().delete()
        Workout.objects.all().delete()
        Activity.objects.all().delete()
        FitUser.objects.all().delete()
        Team.objects.all().delete()

        team_marvel = Team.objects.create(name='Team Marvel', universe='Marvel')
        team_dc = Team.objects.create(name='Team DC', universe='DC')

        users = [
            FitUser(name='Peter Parker', email='spiderman@octofit.com', hero_alias='Spider-Man', team=team_marvel),
            FitUser(name='Tony Stark', email='ironman@octofit.com', hero_alias='Iron Man', team=team_marvel),
            FitUser(name='Bruce Wayne', email='batman@octofit.com', hero_alias='Batman', team=team_dc),
            FitUser(name='Clark Kent', email='superman@octofit.com', hero_alias='Superman', team=team_dc),
        ]
        FitUser.objects.bulk_create(users)

        peter = FitUser.objects.get(email='spiderman@octofit.com')
        tony = FitUser.objects.get(email='ironman@octofit.com')
        bruce = FitUser.objects.get(email='batman@octofit.com')
        clark = FitUser.objects.get(email='superman@octofit.com')

        Activity.objects.bulk_create(
            [
                Activity(user=peter, activity_type='Web Swing Cardio', duration_minutes=45, calories_burned=520, activity_date=date(2026, 2, 20)),
                Activity(user=tony, activity_type='Repulsor HIIT', duration_minutes=40, calories_burned=610, activity_date=date(2026, 2, 20)),
                Activity(user=bruce, activity_type='Gotham Night Run', duration_minutes=50, calories_burned=580, activity_date=date(2026, 2, 21)),
                Activity(user=clark, activity_type='Sky Sprint', duration_minutes=35, calories_burned=700, activity_date=date(2026, 2, 21)),
            ]
        )

        LeaderboardEntry.objects.bulk_create(
            [
                LeaderboardEntry(user=clark, points=980, rank=1),
                LeaderboardEntry(user=tony, points=940, rank=2),
                LeaderboardEntry(user=bruce, points=900, rank=3),
                LeaderboardEntry(user=peter, points=860, rank=4),
            ]
        )

        Workout.objects.bulk_create(
            [
                Workout(user=peter, title='Spider Agility Circuit', focus_area='Agility', difficulty='Medium', recommended_duration=35),
                Workout(user=tony, title='Arc Reactor Strength Set', focus_area='Strength', difficulty='Hard', recommended_duration=45),
                Workout(user=bruce, title='Detective Core Builder', focus_area='Core', difficulty='Medium', recommended_duration=40),
                Workout(user=clark, title='Krypton Endurance Flight', focus_area='Endurance', difficulty='Hard', recommended_duration=30),
            ]
        )

        self.stdout.write(self.style.SUCCESS('octofit_db populated with superhero test data.'))
