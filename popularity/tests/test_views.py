# -*- coding: utf-8 -*-

from django.conf import settings
from django.test import TestCase
from django.core.cache import cache
from django.views.generic import DetailView
from django.test.client import RequestFactory
from django.core.handlers.base import BaseHandler
from django.utils.module_loading import import_string
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.flatpages.models import FlatPage

from model_mommy import mommy

from popularity.views import PopularityMixin


class RequestMock(RequestFactory):

    def request(self, **request):
        request = RequestFactory.request(self, **request)
        handler = BaseHandler()
        handler.load_middleware()
        # call each middleware in turn and throw away any responses that they might return
        for middleware_path in settings.MIDDLEWARE:
            middleware = import_string(middleware_path)(handler)
            if hasattr(middleware, 'process_request'):
                middleware.process_request(request)

        return request


class ViewMock(PopularityMixin, DetailView):
    template_name = 'test.html'
    model = FlatPage

    count_hit = True  # will trigger async hit counting


class PopularityMixinAnonymousTest(TestCase):

    def setUp(self):
        self.object = mommy.make('flatpages.FlatPage')

        self.view = ViewMock.as_view()

        self.request = RequestMock().get('/fake.html')
        self.request.user = AnonymousUser()

    def tearDown(self):
        cache.clear()

    def test_hits(self):
        response = self.view(self.request, pk=self.object.pk)
        self.assertEqual(response.context_data['hitcount']['total_hits'], 0)  # returns cached result

        cache.clear()  # explicitly clear cache

        # second hit, after cache is cleared
        response = self.view(self.request, pk=self.object.pk)
        self.assertEqual(response.context_data['hitcount']['total_hits'], 1)  # returns fresh result


class PopularityMixinAuthenticatedTest(TestCase):

    def setUp(self):
        self.object = mommy.make('flatpages.FlatPage')

        self.view = ViewMock.as_view()

        self.request = RequestMock().get('/fake.html')
        self.request.user = User.objects.create_user('john', password='123')

    def tearDown(self):
        cache.clear()

    def test_hits(self):
        response = self.view(self.request, pk=self.object.pk)
        self.assertEqual(response.context_data['hitcount']['total_hits'], 0)  # returns cached result

        cache.clear()  # explicitly clear cache

        # second hit, after cache is cleared
        response = self.view(self.request, pk=self.object.pk)
        self.assertEqual(response.context_data['hitcount']['total_hits'], 1)  # returns fresh result


class PopularityMixinDisabledTest(TestCase):

    def setUp(self):
        self.object = mommy.make('flatpages.FlatPage')

        self.view = ViewMock.as_view(count_hit=False)

        self.request = RequestMock().get('/fake.html')
        self.request.user = AnonymousUser()

    def tearDown(self):
        cache.clear()

    def test_hits(self):
        response = self.view(self.request, pk=self.object.pk)
        self.assertEqual(response.context_data['hitcount']['total_hits'], 0)  # returns cached result

        cache.clear()  # explicitly clear cache

        # second hit, after cache is cleared
        response = self.view(self.request, pk=self.object.pk)
        self.assertEqual(response.context_data['hitcount']['total_hits'], 0)  # returns fresh result
