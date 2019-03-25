# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.cache import cache

from model_mommy import mommy


class PopularityTagTest(TestCase):

    html = """{% load popularity_tags %}{% get_hit_count for object as hits %}Total: {{ hits }} hits"""

    @property
    def template(self):
        from django.template import engines

        return engines['django'].from_string(self.html)

    def setUp(self):
        self.object = mommy.make('flatpages.FlatPage')

    def tearDown(self):
        cache.clear()

    def test_default(self):
        self.assertTrue("Total: 0 hits" in self.template.render({'object': self.object}))
