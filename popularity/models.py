# -*- coding: utf-8 -*-

from django.dispatch import receiver
from django.db.models.signals import post_save

from hitcount.models import Hit

from .tasks import HitCountJob


@receiver(post_save, sender=Hit)
def invalidate(sender, instance, **kwargs):
    if 'created' in kwargs and kwargs['created'] is True:
        opts, object_id = instance._meta, instance.pk,
        # invalidate cache...
        HitCountJob().invalidate(
            opts.app_label, opts.module_name, object_id)
