# -*- coding: utf-8 -*-

from django.conf import settings

from tasks import update_hitcount, HitCount

__all__ = ['PopularityMixin']


class PopularityMixin(object):

    def get(self, request, *args, **kwargs):
        response = super(PopularityMixin, self).get(request, *args, **kwargs)
        if getattr(settings, 'USE_HITCOUNT', False):
            from hitcount.utils import get_ip

            opts, object_id = self.object._meta, self.object.pk

            if not request.session.session_key:
                request.session.save()

            session_key, ip_address = request.session.session_key, get_ip(request)
            username = request.user.username if request.user.is_authenticated() else None
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]

            update_hitcount.delay(session_key, ip_address, user_agent, username, opts.app_label, opts.module_name, object_id)
        return response

    def get_hitcount_for(self, obj):
        opts, object_id = obj._meta, obj.pk
        return HitCount().get(opts.app_label, opts.module_name, object_id)
