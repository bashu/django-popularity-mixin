# -*- coding: utf-8 -*-

from django.contrib.auth.models import User
from django.views.generic import DetailView
from django.conf.urls.defaults import patterns, url

from popularity.views import PopularityMixin


class UserDetail(PopularityMixin, DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super(UserDetail, self).get_context_data(**kwargs)
        if self.object.is_active is True:
            context.update({'hitcount': self.get_hitcount_for(self.object)})
        return context


urlpatterns = patterns('',
    url(r'^(?P<pk>\d+)/', UserDetail.as_view(), name='user_detail'),
)
