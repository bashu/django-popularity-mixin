# -*- coding: utf-8 -*-

from django.test import TestCase
from django.contrib.auth.models import User


class PopularityMixinTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('john', 'john@foo.com', '123')

    def test_default(self):
        pass
