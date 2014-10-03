# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import AnonymousUser, User

from hitcount.models import Hit, HitCount, BlacklistIP, BlacklistUserAgent


@transaction.atomic
def update_hitcount(session_key, ip_address, user_agent, username, app_label, model, object_id):

    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        user = AnonymousUser()

    ctype = ContentType.objects.get(app_label=app_label, model=model)

    hitcount, created = HitCount.objects.get_or_create(
        content_type=ctype, object_pk=object_id)

    hits_per_ip_limit = getattr(settings, 'HITCOUNT_HITS_PER_IP_LIMIT', 0)
    exclude_user_group = getattr(settings, 'HITCOUNT_EXCLUDE_USER_GROUP', None)

    # first, check our request against the blacklists before continuing
    if BlacklistIP.objects.filter(ip__exact=ip_address) or \
            BlacklistUserAgent.objects.filter(user_agent__exact=user_agent):
        return False

    # second, see if we are excluding a specific user group or not
    if exclude_user_group and user.is_authenticated():
        if user.groups.filter(name__in=exclude_user_group):
            return False

    # start with a fresh active query set (HITCOUNT_KEEP_HIT_ACTIVE )
    qs = Hit.objects.filter_active()

    # check limit on hits from a unique ip address (HITCOUNT_HITS_PER_IP_LIMIT)
    if hits_per_ip_limit:
        if qs.filter(ip__exact=ip_address).count() > hits_per_ip_limit:
            return False

    # create a generic Hit object with request data
    hit = Hit(session=session_key, hitcount=hitcount, ip=ip_address,
              user_agent=user_agent)

    # first, use a user's authentication to see if they made an earlier hit
    if user.is_authenticated():
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
