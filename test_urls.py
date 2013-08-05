# -*- coding: utf-8 -*-

from django.views.generic import DetailView
from django.contrib.sites.models import Site
from django.conf.urls.defaults import patterns, url

from popularity.views import PopularityMixin


class TestView(PopularityMixin, DetailView):
    template_name = 'test.html'
    model = Site

    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        context.update({'hitcount': self.get_hitcount_for(self.object)})
        return context

urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/', TestView.as_view(), name='test_view'),
)
