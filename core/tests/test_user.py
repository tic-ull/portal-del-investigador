# -*- encoding: UTF-8 -*-

from core.models import UserProfile
from django.test import TestCase
from factories import UserFactory


class UserTests(TestCase):

    def test_user_profile_created_on_user_creation(self):
        user = UserFactory.create()
        profile = UserProfile.objects.filter(user__username=user.username)
        self.assertEqual(len(profile), 1)
