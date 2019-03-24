# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.cache import cache

from model_mommy import mommy


class PopularityTagTest(TestCase):

    html = """{% load popularity_tags %}{% get_hitcount for object as hitcount %}Total: {{ hitcount.total }}, today: {{ hitcount.today }}"""

    @property
    def template(self):
        from django.template import engines

        return engines['django'].from_string(self.html)

    def setUp(self):
        self.object = mommy.make('flatpages.FlatPage')

    def tearDown(self):
        cache.clear()

    def test_default(self):
        self.assertTrue("Total: 0, today: 0" in self.template.render({'object': self.object}))
