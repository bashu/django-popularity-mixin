# -*- coding: utf-8 -*-

from django.test import TestCase
from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from ..tasks import HitCountJob


class PopularityAnonymousTest(TestCase):

    def setUp(self):
        self.base_url = 'http://testserver'

        self.object = User.objects.create_user('john', 'john@foo.com', '123')

    def tearDown(self):
        cache.clear()

    def test_anonymous(self):
        opts, object_id = self.object._meta, self.object.pk

        hits = HitCountJob().get(opts.app_label, opts.module_name, object_id)
        self.assertEqual(hits['total'], 0)

        self.client.get(reverse('test_detail', args=[object_id]))

        hits = HitCountJob().get(opts.app_label, opts.module_name, object_id)
        self.assertEqual(hits['total'], 0)  # returns cached result

        cache.clear()  # clear cache

        hits = HitCountJob().get(opts.app_label, opts.module_name, object_id)
        self.assertEqual(hits['total'], 1)  # returns fresh results

        # second hit
        self.client.get(reverse('test_detail', args=[object_id]))

        cache.clear()  # clear cache

        hits = HitCountJob().get(opts.app_label, opts.module_name, object_id)
        self.assertEqual(hits['total'], 1)  # returns fresh results

    def test_context_data(self):
        opts, object_id = self.object._meta, self.object.pk

        response = self.client.get(reverse('test_detail', args=[object_id]))
        self.assertEqual(response.context['hitcount'], {'total': 0, 'today': 0})


class PopularityAuthenticatedTest(TestCase):

    def setUp(self):
        self.base_url = 'http://testserver'

        self.object = User.objects.create_user('john', 'john@foo.com', '123')
        self.client.login(username='john', password='123')

    def tearDown(self):
        cache.clear()

    def test_authenticated(self):
        opts, object_id = self.object._meta, self.object.pk

        hits = HitCountJob().get(opts.app_label, opts.module_name, object_id)
        self.assertEqual(hits['total'], 0)

        self.client.get(reverse('test_detail', args=[object_id]))

        hits = HitCountJob().get(opts.app_label, opts.module_name, object_id)
        self.assertEqual(hits['total'], 0)  # returns cached result

        cache.clear()  # clear cache

        hits = HitCountJob().get(opts.app_label, opts.module_name, object_id)
        self.assertEqual(hits['total'], 1)  # returns fresh results

        # second hit
        self.client.get(reverse('test_detail', args=[object_id]))

        cache.clear()  # clear cache

        hits = HitCountJob().get(opts.app_label, opts.module_name, object_id)
        self.assertEqual(hits['total'], 1)  # returns fresh results

    def test_context_data(self):
        opts, object_id = self.object._meta, self.object.pk

        response = self.client.get(reverse('test_detail', args=[object_id]))
        self.assertEqual(response.context['hitcount'], {'total': 0, 'today': 0})


class PopularityDisabledTest(TestCase):

    def setUp(self):
        self.base_url = 'http://testserver'

        self.old_USE_HITCOUNT = settings.USE_HITCOUNT
        settings.USE_HITCOUNT = False
        self.object = User.objects.create_user('john', 'john@foo.com', '123')

    def tearDown(self):
        settings.USE_HITCOUNT = self.old_USE_HITCOUNT
        cache.clear()

    def test_context_data(self):
        opts, object_id = self.object._meta, self.object.pk

        response = self.client.get(reverse('test_detail', args=[object_id]))
        self.assertEqual(response.context['hitcount'], None)
