from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils.translation import ugettext as _

from notification import models as notifications
from toggleproperties.models import ToggleProperty

from astrobin.models import Request
from astrobin.models import Gear
from astrobin.models import Image

from nested_comments.models import NestedComment


def privatebeta_enabled(request):
    return {'privatebeta_enabled': settings.PRIVATEBETA_ENABLE_BETA}


def notices_count(request):
    response = {}
    if request.user.is_authenticated():
        response['notifications_count'] = notifications.Notice.objects.filter(Q(recipient = request.user) & Q(unseen = True)).count()

    return response


def user_language(request):
    d = {
        'user_language': request.LANGUAGE_CODE,
    }
    if request.user.is_authenticated():
        profile = request.user.userprofile
        d['user_language'] = profile.language

    return d


def user_profile(request):
    d = {
        'userprofile': None,
    }

    if request.user.is_authenticated():
        profile = request.user.userprofile
        d['userprofile'] = profile

    return d


def user_scores(request):
    scores = {
        'user_scores_likes': 0,
        'user_scores_images': 0,
        'user_scores_comments': 0,
        'user_scores_followers': 0,
    }

    if request.user.is_authenticated():
        cache_key = "astrobin_user_score_%s" % request.user
        scores = cache.get(cache_key)
        user = User.objects.get(pk = request.user.pk) # The lazy object in the request won't do

        if not scores:
            scores = {}
            all_images = Image.objects.filter(user = request.user, is_wip = False)

            likes = 0
            for i in all_images:
                likes += ToggleProperty.objects.toggleproperties_for_object("like", i).count()

            profile = request.user.userprofile
            followers = ToggleProperty.objects.toggleproperties_for_object("follow", user).count()


            scores['user_scores_likes'] = likes
            scores['user_scores_images'] = all_images.count()
            scores['user_scores_comments'] =  NestedComment.objects.filter(author = request.user, deleted = False).count()
            scores['user_scores_followers'] = followers
            cache.set(cache_key, scores, 600)

    return scores


def common_variables(request):
    from rawdata.utils import user_has_subscription

    d = {
        #'random_gear_item': Gear.objects.filter(moderator_fixed = None).order_by('?')[:1].get(),
        'is_producer': request.user.groups.filter(name='Producers'),
        'is_retailer': request.user.groups.filter(name='Retailers'),
        'has_rawdata_subscription': user_has_subscription(request.user),
        'IMAGES_URL' : settings.IMAGES_URL,
        'CDN_URL' : settings.CDN_URL,
    }

    return d

