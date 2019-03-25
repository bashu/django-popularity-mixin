# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

from celery.task import task
from cacheback.base import Job

from hitcount.models import HitCount

from .utils import update_hitcount


@task(ignore_result=True)
def celery_update_hitcount(
        session_key, ip_address, user_agent, user_id, app_label, model, object_id):

    return update_hitcount(
        session_key, ip_address, user_agent, user_id, app_label, model, object_id)


class HitCountJob(Job):

    def __init__(self, *args, **kwargs):
        self.lifetime = getattr(settings, 'HITCOUNT_REFRESH_INTERVAL', 600)
        return super(HitCountJob, self).__init__(*args, **kwargs)

    def fetch(self, app_label, model, object_id):
        ctype = ContentType.objects.get(app_label=app_label, model=model)

        hit_count, created = HitCount.objects.get_or_create(
            content_type=ctype, object_pk=object_id)

        return hit_count
