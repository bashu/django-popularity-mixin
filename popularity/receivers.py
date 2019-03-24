# -*- coding: utf-8 -*-

from django.db import models
from django.dispatch import receiver

from hitcount.models import Hit

from .tasks import HitCountJob


@receiver(models.signals.post_save, sender=Hit)
def invalidate_cache(sender, instance, **kwargs):
    if 'created' in kwargs and kwargs['created'] is True:
        opts, object_id = instance._meta, instance.pk,
        HitCountJob().invalidate(opts.app_label, opts.model_name, object_id)
