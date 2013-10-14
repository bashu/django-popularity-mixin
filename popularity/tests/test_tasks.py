# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.cache import cache

from model_mommy import mommy

from popularity.tasks import HitCountJob


class HitCountJobTest(TestCase):

    def setUp(self):
        self.object = mommy.make('flatpages.FlatPage')
        self.job = HitCountJob()

    def tearDown(self):
        cache.clear()

    def test_caching(self):
        opts, object_id = self.object._meta, self.object.pk

        # first hit...
        with self.assertNumQueries(2):
            hits = self.job.get(opts.app_label, opts.module_name, object_id)

        self.assertEqual(hits['total'], 0)

        # second hit...
        with self.assertNumQueries(0):
            hits = self.job.get(opts.app_label, opts.module_name, object_id)

        self.assertEqual(hits['total'], 0)  # returns cached result
