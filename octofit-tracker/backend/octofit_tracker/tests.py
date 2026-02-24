from django.test import TestCase
from django.urls import reverse


class ApiRootTests(TestCase):
    def test_api_root_route_exists(self):
        response = self.client.get(reverse('api-root'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
        self.assertIn('activities', response.data)
        self.assertIn('leaderboard', response.data)
        self.assertIn('workouts', response.data)

    def test_root_points_to_api(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('users', response.data)
        self.assertIn('teams', response.data)
