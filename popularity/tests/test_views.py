# -*- coding: utf-8 -*-

from django.conf import settings
from django.test import TestCase
from django.core.cache import cache
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse


class PopularityAnonymousTest(TestCase):

    def setUp(self):
        self.base_url = 'http://testserver'

        obj = Site.objects.get_or_create(pk=settings.SITE_ID)[0]
        self.detail_url = reverse('test_view', args=[obj.pk])

    def tearDown(self):
        cache.clear()

    def test_hits(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.context['hitcount']['total'], 0)  # returns cached result

        cache.clear()  # clear cache

        # second hit
        response = self.client.get(self.detail_url)

        self.assertEqual(response.context['hitcount']['total'], 1)  # returns fresh result

    def test_context_data(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.context['hitcount'], {'total': 0, 'today': 0})


class PopularityAuthenticatedTest(TestCase):
    fixtures = ['users']

    def setUp(self):
        self.base_url = 'http://testserver'

        obj = Site.objects.get_or_create(pk=settings.SITE_ID)[0]
        self.detail_url = reverse('test_view', args=[obj.pk])

        self.client.login(username='john', password='123')

    def tearDown(self):
        cache.clear()

    def test_hits(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.context['hitcount']['total'], 0)  # returns cached result

        cache.clear()  # clear cache

        # second hit
        response = self.client.get(self.detail_url)

    def test_context_data(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.context['hitcount'], {'total': 0, 'today': 0})


class PopularityDisabledTest(TestCase):

    def setUp(self):
        self.base_url = 'http://testserver'

        obj = Site.objects.get_or_create(pk=settings.SITE_ID)[0]
        self.detail_url = reverse('test_view', args=[obj.pk])

        self.old_USE_HITCOUNT = settings.USE_HITCOUNT
        settings.USE_HITCOUNT = False

    def tearDown(self):
        settings.USE_HITCOUNT = self.old_USE_HITCOUNT
        cache.clear()

    def test_context_data(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.context['hitcount'], None)
