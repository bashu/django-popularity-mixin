# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

from hitcount.models import Hit, HitCount, BlacklistIP, BlacklistUserAgent


@transaction.atomic
def update_hitcount(session_key, ip_address, user_agent, user_id, app_label, model, object_id):

    try:
        user = get_user_model().objects.get(pk=user_id)
    except ObjectDoesNotExist:
        user = AnonymousUser()

    ctype = ContentType.objects.get(app_label=app_label, model=model)

    hitcount, created = HitCount.objects.get_or_create(
        content_type=ctype, object_pk=object_id)

    hits_per_ip_limit = getattr(settings, 'HITCOUNT_HITS_PER_IP_LIMIT', 0)
    exclude_user_group = getattr(settings, 'HITCOUNT_EXCLUDE_USER_GROUP', None)

    # first, check our request against the IP blacklist
    if BlacklistIP.objects.filter(ip__exact=ip_address):
        return False

    # second, check our request against the user agent blacklist
    if BlacklistUserAgent.objects.filter(user_agent__exact=user_agent):
        return False

    # third, see if we are excluding a specific user group or not
    if exclude_user_group and not isinstance(user, AnonymousUser):
        if user.groups.filter(name__in=exclude_user_group):
            return False

    # eliminated first three possible exclusions, now on to checking our database of
    # active hits to see if we should count another one
    
    # start with a fresh active query set (HITCOUNT_KEEP_HIT_ACTIVE)
    qs = Hit.objects.filter_active()

    # check limit on hits from a unique ip address (HITCOUNT_HITS_PER_IP_LIMIT)
    if hits_per_ip_limit:
        if qs.filter(ip__exact=ip_address).count() >= hits_per_ip_limit:
            return False

    # create a generic Hit object with request data
    hit = Hit(session=session_key, hitcount=hitcount, ip=ip_address,
              user_agent=user_agent)

    # first, use a user's authentication to see if they made an earlier hit
    if not isinstance(user, AnonymousUser):
        if not qs.filter(user=user, hitcount=hitcount):
            hit.user = user  # associate this hit with a user
            hit.save()

            return True

    # if not authenticated, see if we have a repeat session
    else:
        if not qs.filter(session=session_key, hitcount=hitcount):
            hit.save()

            return True

    return False
