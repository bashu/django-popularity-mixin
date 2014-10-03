# -*- coding: utf-8 -*-

from django import template
from django.conf import settings

from classytags.core import Tag, Options
from classytags.arguments import Argument

from ..tasks import HitCountJob

register = template.Library()


class PopularityTag(Tag):
    name = 'get_hitcount'
    options = Options(
        'for',
        Argument('instance', required=True),
        'as',
        Argument('varname', resolve=False, required=False),
    )

    def render_tag(self, context, instance, varname):
        if getattr(settings, 'USE_HITCOUNT', False):
            opts, pk = instance._meta, instance.pk
            hitcount = HitCountJob().get(opts.app_label, opts.model_name, pk)
        else:
            hitcount = None

        if varname:
            context[varname] = hitcount
            return ''
        else:
            return hitcount

register.tag(PopularityTag)
