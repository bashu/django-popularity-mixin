# -*- coding: utf-8 -*-

from django.db.models.base import Model

from hitcount.utils import get_ip

from popularity.tasks import celery_update_hitcount


class PopularityMixin(object):

    count_hit = False

    def get(self, request, *args, **kwargs):
        response = super(PopularityMixin, self).get(request, *args, **kwargs)

        if self.count_hit is False:
            return response

        if hasattr(self, 'object') and isinstance(self.object, Model): # hey we got a model instance
            opts, u = self.object._meta, request.user
            
            if not request.session.session_key:
                request.session.save()

            try:
                is_authenticated = u.is_authenticated()
            except:
                is_authenticated = u.is_authenticated

            celery_update_hitcount.delay(
                session_key=request.session.session_key,
                ip_address=get_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
                user_id=u.pk if is_authenticated else None,
                app_label=opts.app_label,
                model=opts.model_name,
                object_id=self.object.id,
            )

        return response

    def get_context_data(self, **kwargs):
        context = super(PopularityMixin, self).get_context_data(**kwargs)

        if hasattr(self, 'object') and isinstance(self.object, Model): # hey we got a model instance
            from popularity.tasks import HitCountJob

            opts, pk = self.object._meta, self.object.pk
            hit_count = HitCountJob().get(opts.app_label, opts.model_name, pk)

            context['hitcount'] = {'pk': hit_count.pk, 'total_hits': hit_count.hits}

        return context
