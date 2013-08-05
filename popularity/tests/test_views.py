# -*- coding: utf-8 -*-

from django.conf import settings
from django.test import TestCase
from django.core.cache import cache
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from ..tasks import HitCountJob


class PopularityAnonymousTest(TestCase):

    def setUp(self):
        self.base_url = 'http://testserver'
        self.object = Site.objects.get_or_create(pk=settings.SITE_ID)[0]

        self.job = HitCountJob()

    def tearDown(self):
        cache.clear()

    def test_anonymous(self):
        opts, object_id = self.object._meta, self.object.pk

        hits = self.job.get(opts.app_label, opts.module_name, object_id)
        self.assertEqual(hits['total'], 0)

        response = self.client.get(reverse('test_view', args=[object_id]))

        hits = self.job.get(opts.app_label, opts.module_name, object_id)
        self.assertEqual(hits['total'], 0)  # returns cached result

        cache.clear()  # clear cache

        hits = self.job.get(opts.app_label, opts.module_name, object_id)
        self.assertEqual(hits['total'], 1)  # returns fresh results

        # second hit
        response = self.client.get(reverse('test_view', args=[object_id]))

        cache.clear()  # clear cache

        hits = self.job.get(opts.app_label, opts.module_name, object_id)
        self.assertEqual(hits['total'], 1)  # returns fresh results

    def test_context_data(self):
        opts, object_id = self.object._meta, self.object.pk

        response = self.client.get(reverse('test_view', args=[object_id]))
        self.assertEqual(response.context['hitcount'], {'total': 0, 'today': 0})


class PopularityAuthenticatedTest(TestCase):
    fixtures = ['accounts']

    def setUp(self):
        self.base_url = 'http://testserver'
        self.object = Site.objects.get_or_create(pk=settings.SITE_ID)[0]

        self.client.login(username='john', password='123')

        self.job = HitCountJob()

    def tearDown(self):
        cache.clear()

    def test_authenticated(self):
        opts, object_id = self.object._meta, self.object.pk

        hits = self.job.get(opts.app_label, opts.module_name, object_id)
        self.assertEqual(hits['total'], 0)

        response = self.client.get(reverse('test_view', args=[object_id]))

        hits = self.job.get(opts.app_label, opts.module_name, object_id)
        self.assertEqual(hits['total'], 0)  # returns cached result

        cache.clear()  # clear cache

        hits = self.job.get(opts.app_label, opts.module_name, object_id)
        self.assertEqual(hits['total'], 1)  # returns fresh results

        # second hit
        response = self.client.get(reverse('test_view', args=[object_id]))

        cache.clear()  # clear cache

        hits = self.job.get(opts.app_label, opts.module_name, object_id)
        self.assertEqual(hits['total'], 1)  # returns fresh results

    def test_context_data(self):
        opts, object_id = self.object._meta, self.object.pk

        response = self.client.get(reverse('test_view', args=[object_id]))
        self.assertEqual(response.context['hitcount'], {'total': 0, 'today': 0})


class PopularityDisabledTest(TestCase):

    def setUp(self):
        self.base_url = 'http://testserver'

        self.old_USE_HITCOUNT = settings.USE_HITCOUNT
        settings.USE_HITCOUNT = False
        self.object = Site.objects.get_or_create(pk=settings.SITE_ID)[0]

    def tearDown(self):
        settings.USE_HITCOUNT = self.old_USE_HITCOUNT
        cache.clear()

    def test_context_data(self):
        opts, object_id = self.object._meta, self.object.pk

        response = self.client.get(reverse('test_view', args=[object_id]))
        self.assertEqual(response.context['hitcount'], None)
