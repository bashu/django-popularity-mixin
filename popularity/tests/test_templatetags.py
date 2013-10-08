# -*- coding: utf-8 -*-

from django.conf import settings
from django.test import TestCase
from django.core.cache import cache
from django.contrib.sites.models import Site
from django.template import loader, Context


class PopularityTagTest(TestCase):

    html = """{% load popularity_tags %}{% get_hitcount for object as hitcount %}Total: {{ hitcount.total }}, today: {{ hitcount.today }}"""

    @property
    def tt(self):
        return loader.get_template_from_string(self.html)

    def setUp(self):
        self.object = Site.objects.get_or_create(pk=settings.SITE_ID)[0]

    def tearDown(self):
        cache.clear()

    def test_default(self):
        self.assertTrue("Total: 0, today: 0" in self.tt.render(Context({
            'object': self.object})))
