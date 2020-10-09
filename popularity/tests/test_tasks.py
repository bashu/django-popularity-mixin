# -*- coding: utf-8 -*-

from django.core.cache import cache
from django.test import TestCase
from model_mommy import mommy

from popularity.tasks import HitCountJob


class HitCountJobTest(TestCase):
    def setUp(self):
        self.object = mommy.make("flatpages.FlatPage")

    def tearDown(self):
        cache.clear()

    def test_caching(self):
        opts, object_id = self.object._meta, self.object.pk
        job = HitCountJob()

        # first hit...
        with self.assertNumQueries(5):
            hit_count = job.get(opts.app_label, opts.model_name, object_id)

        self.assertEqual(hit_count.hits, 0)  # first run, nothing yet

        # second hit, will return cached result...
        with self.assertNumQueries(0):  # nothing in background
            hit_count = job.get(opts.app_label, opts.model_name, object_id)

        self.assertEqual(hit_count.hits, 0)  # returns cached result

    def test_refresh_interval(self):
        # overriding default settings...
        with self.settings(HITCOUNT_REFRESH_INTERVAL=0):
            opts, object_id = self.object._meta, self.object.pk
            job = HitCountJob()

            # first hit...
            with self.assertNumQueries(5):
                hit_count = job.get(opts.app_label, opts.model_name, object_id)

            self.assertEqual(hit_count.hits, 0)  # first run, nothing yet

            # second hit, will return stale result, but starts async
            # refreshing...
            with self.assertNumQueries(2):  # aha, we do make queries
                hit_count = job.get(opts.app_label, opts.model_name, object_id)

            self.assertEqual(hit_count.hits, 0)  # returns cached result
