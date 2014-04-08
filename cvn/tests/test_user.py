from django.test import TestCase
from cvn.models import UserProfile
from factories import UserFactory


class UserTests(TestCase):

    def test_user_profile_created_on_user_creation(self):
        u = UserFactory.create()
        profile = UserProfile.objects.filter(user__username=u.username)
        self.assertEqual(len(profile), 1)
