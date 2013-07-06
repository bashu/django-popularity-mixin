# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.conf.urls.defaults import patterns, url

from popularity.views import PopularityMixin


class TestDetail(PopularityMixin, DetailView):
    template_name = 'test_detail.html'
    model = User

    def get_context_data(self, **kwargs):
        context = super(TestDetail, self).get_context_data(**kwargs)
        if self.object.is_active is True:
            context.update({'hitcount': self.get_hitcount_for(self.object)})
        return context


urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/', TestDetail.as_view(), name='test_detail'),
)
