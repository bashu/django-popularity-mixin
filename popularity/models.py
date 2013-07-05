# -*- coding: utf-8 -*-

from django.dispatch import receiver
from django.db.models.signals import post_save

from hitcount.models import Hit

from .tasks import HitCountJob


@receiver(post_save, sender=Hit)
def invalidate(sender, instance, **kwargs):
    if instance is not None and isinstance(instance, Hit):
        opts, object_id = instance._meta, instance.pk,
        HitCountJob().invalidate(opts.app_label, opts.module_name, object_id)
