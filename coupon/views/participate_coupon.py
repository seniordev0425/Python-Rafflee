"""
    Creation of coupon
"""

import logging
import random
import twitter
import requests
import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from analytics.models.promotion_numbers import PromotionNumbers
from account.models import MyUser
from coupon.models import Coupon
from promotion.models import Promotion
from promotion.models.promotion import Response as PollResponse
from rafflee import settings
from social_network.models.user_social_action import UserSocialAction
from tools.json import ApiJsonResponse
from tools.serializer import serialize_coupon_object, serialize_winning_object_for_user

logger = logging.getLogger("django")


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_result_by_promotion(request, id):
    """
    API endpoint for getting the result of a promotion
    Args:
        request:
        id: id of the promotion
    Returns: coupon object
    """
    response = ApiJsonResponse()
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=id)
    except Exception as e:
        return Response({
            "msg": _('MSG_NO_PROMOTION_FOUNDED'),
            "status": 404
        }, status=404)
    try:
        coupon = Coupon.objects.get(promotion=promotion, user=user, distributed=True)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_COUPON_NOT_EXIST'),
            "status": 404
        }, status=404)
    if not coupon.visible:
        if promotion.type_of_distribution == 'end_promotion':
            if timezone.now() < promotion.end_date:
                return Response({
                    "msg": _('MSG_PROMOTION_STILL_IN_PROGRESS'),
                    "status": 404
                }, status=404)
            else:
                coupon.visible = True
                coupon.save()
                response.set_data(serialize_coupon_object(coupon))
        else:
            return Response({
                "msg": _('MSG_WINNING_WILL_BE_DISTRIBUTED_DURING_THE_LIVE'),
                "status": 404
            }, status=404)
    else:
        try:
            winning_object = promotion.winnings.get(name=coupon.name)
        except ObjectDoesNotExist:
            return Response({
                "msg": _('MSG_NO_WINNING_OBJECT'),
                "status": 500
            }, status=500)
        response.set_data(serialize_winning_object_for_user(winning_object, promotion))
    response.set_result_code(200)
    response.set_result_msg("MSG_WINNING_OBJECT_FOUNDED")
    return JsonResponse(response.get_dict())


def verification_validation_action(user, promotion):
    if user.company_account:
        return 404, "MSG_IMPOSSIBLE_TO_PARTICIPATE_WITH_PRO_ACCOUNT"
    if not user.phone_number_verification:
        return 404, "MSG_PHONE_NUMBER_NOT_CONFIRMED"
    if promotion.type_of_distribution == 'giveaway':
        if promotion.number_of_maximum_participants:
            if promotion.number_of_participants >= promotion.number_of_maximum_participants:
                try:
                    promotion.participants.get(pk=user.pk)
                    return 200, "VERIFICATION_OK"
                except Exception as e:
                    return 404, "MSG_MAXIMUM_NUMBER_OF_USERS_REACHED"
    return 200, "VERIFICATION_OK"


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def poll(request):
    """
    This function validate the poll action
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
        response = request.data['response']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.poll:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    try:
        social_action = UserSocialAction.objects.get(user=user, promotion=promotion)
    except UserSocialAction.DoesNotExist:
        social_action = UserSocialAction.objects.create(user=user, promotion=promotion)
    if social_action.poll:
        return Response({
            "msg": _('MSG_ERROR_ACTION_ALREADY_VALIDATED'),
            "status": 404
        }, status=404)
    try:
        promotion.result_poll.add(PollResponse.objects.create(response=response, user=user))
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_WITH_ACTION'),
            "status": 404
        }, status=404)
    social_action.poll = True
    social_action.entries = social_action.entries + promotion.social_action.entries.pool_entries
    social_action.save()
    try:
        analytics = PromotionNumbers.objects.filter(promotion=promotion).last()
        analytics.click_actions = analytics.click_actions + 1
        analytics.save()
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_WITH_ANALYTICS'),
            "status": 404
        }, status=404)
    return Response({
        "entries": social_action.entries,
        "msg": _('MSG_VALIDATED_RESPONSE'),
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def url_website(request):
    """
    This function validate the click on website url action
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.website:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    try:
        social_action = UserSocialAction.objects.get(user=user, promotion=promotion)
    except UserSocialAction.DoesNotExist:
        social_action = UserSocialAction.objects.create(user=user, promotion=promotion)
    if social_action.website:
        return Response({
            "msg": _('MSG_ERROR_ACTION_ALREADY_VALIDATED'),
            "status": 404
        }, status=404)
    social_action.website = True
    social_action.entries = social_action.entries + promotion.social_action.entries.website_entries
    social_action.save()
    try:
        analytics = PromotionNumbers.objects.filter(promotion=promotion).last()
        analytics.click_actions = analytics.click_actions + 1
        analytics.save()
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_WITH_ANALYTICS'),
            "status": 404
        }, status=404)
    return Response({
        "entries": social_action.entries,
        "msg": _('MSG_VALIDATED_URL_WEBSITE'),
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def url_video(request):
    """
    This function validate the watching url video action
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.video:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    try:
        social_action = UserSocialAction.objects.get(user=user, promotion=promotion)
    except UserSocialAction.DoesNotExist:
        social_action = UserSocialAction.objects.create(user=user, promotion=promotion)
    if social_action.video:
        return Response({
            "msg": _('MSG_ERROR_ACTION_ALREADY_VALIDATED'),
            "status": 404
        }, status=404)
    social_action.video = True
    social_action.entries = social_action.entries + promotion.social_action.entries.video_entries
    social_action.save()
    try:
        analytics = PromotionNumbers.objects.get(promotion=promotion)
        analytics.click_actions = analytics.click_actions + 1
        analytics.save()
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_WITH_ANALYTICS'),
            "status": 404
        }, status=404)
    try:
        analytics = PromotionNumbers.objects.filter(promotion=promotion).last()
        analytics.click_actions = analytics.click_actions + 1
        analytics.save()
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_WITH_ANALYTICS'),
            "status": 404
        }, status=404)
    return Response({
        "entries": social_action.entries,
        "msg": _('MSG_VALIDATED_VIDEO'),
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def twitter_tweet_validation(request):
    """
    This function validate the twitter tweet action
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.twitter_tweet:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    if not user.social_connection.twitter_connected:
        return Response({
            "msg": _('MSG_ERROR_USER_NOT_CONNECTED_TO_TWITTER'),
            "status": 404
        }, status=404)
    try:
        social_action = UserSocialAction.objects.get(user=user, promotion=promotion)
    except UserSocialAction.DoesNotExist:
        social_action = UserSocialAction.objects.create(user=user, promotion=promotion)
    if social_action.twitter_tweet:
        return Response({
            "msg": _('MSG_ERROR_ACTION_ALREADY_VALIDATED'),
            "status": 404
        }, status=404)
    try:
        api = twitter.Api(consumer_key=settings.TWITTER_API_KEY,
                          consumer_secret=settings.TWITTER_API_SECRET_KEY,
                          access_token_key=user.social_connection.twitter_oauth_token_data,
                          access_token_secret=user.social_connection.twitter_oauth_token_secret)
        api.PostUpdate(promotion.social_action.twitter_tweet_model)
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_WITH_TWITTER_TWEET'),
            "status": 404
        }, status=404)
    social_action.twitter_tweet = True
    social_action.entries = social_action.entries + promotion.social_action.entries.twitter_tweet_entries
    social_action.save()
    try:
        analytics = PromotionNumbers.objects.filter(promotion=promotion).last()
        analytics.click_actions = analytics.click_actions + 1
        analytics.save()
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_WITH_ANALYTICS'),
            "status": 404
        }, status=404)
    return Response({
        "entries": social_action.entries,
        "msg": _('MSG_TWITTER_TWEET_VALIDATED'),
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def twitter_like(request):
    """
    This function permit to follow an twitter account
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.twitter_like:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    if not user.social_connection.twitter_connected:
        return Response({
            "msg": _('MSG_ERROR_USER_NOT_CONNECTED_TO_TWITTER'),
            "status": 404
        }, status=404)
    try:
        api = twitter.Api(consumer_key=settings.TWITTER_API_KEY,
                          consumer_secret=settings.TWITTER_API_SECRET_KEY,
                          access_token_key=promotion.company.owner.social_connection.twitter_oauth_token_data,
                          access_token_secret=promotion.company.owner.social_connection.twitter_oauth_token_secret)
        tweet = api.GetStatus(status_id=promotion.social_action.twitter_like_id)
    except Exception as e:
        return Response({
            "msg": _('MSG_ERROR_WITH_TWITTER_LIKE'),
            "status": 404
        }, status=404)
    if tweet.favorited:
        try:
            social_action = UserSocialAction.objects.get(user=user, promotion=promotion)
            social_action.twitter_like = True
            social_action.save()
        except UserSocialAction.DoesNotExist:
            UserSocialAction.objects.create(user=user, promotion=promotion, twitter_like=True)
        return Response({
            "msg": _('MSG_YOU_HAVE_ALREADY_LIKE_THIS_TWEET'),
            "status": 200
        }, status=200)
    return Response({
        "msg": _('MSG_LIKE_VALIDATED'),
        "text": tweet.text,
        "retweet": tweet.retweet_count,
        "like": tweet.favorite_count,
        "created_at": tweet.created_at,
        "name": tweet.user.name,
        "profile_img": tweet.user.profile_image_url_https,
        "verified": tweet.user.verified,
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def twitter_like_validation(request):
    """
    This function permit to follow an twitter account
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.twitter_like:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    if not user.social_connection.twitter_connected:
        return Response({
            "msg": _('MSG_ERROR_USER_NOT_CONNECTED_TO_TWITTER'),
            "status": 404
        }, status=404)
    try:
        social_action = UserSocialAction.objects.get(user=user, promotion=promotion)
    except UserSocialAction.DoesNotExist:
        social_action = UserSocialAction.objects.create(user=user, promotion=promotion)
    if social_action.twitter_like:
        return Response({
            "msg": _('MSG_ERROR_ACTION_ALREADY_VALIDATED'),
            "status": 404
        }, status=404)
    try:
        api = twitter.Api(consumer_key=settings.TWITTER_API_KEY,
                          consumer_secret=settings.TWITTER_API_SECRET_KEY,
                          access_token_key=user.social_connection.twitter_oauth_token_data,
                          access_token_secret=user.social_connection.twitter_oauth_token_secret)
        api.CreateFavorite(status_id=promotion.social_action.twitter_like_id)
    except Exception as e:
        return Response({
            "msg": _('MSG_ERROR_WITH_TWITTER_LIKE'),
            "status": 404
        }, status=404)
    social_action.twitter_like = True
    social_action.entries = social_action.entries + promotion.social_action.entries.twitter_like_entries
    social_action.save()
    try:
        analytics = PromotionNumbers.objects.filter(promotion=promotion).last()
        analytics.click_actions = analytics.click_actions + 1
        analytics.save()
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_WITH_ANALYTICS'),
            "status": 404
        }, status=404)
    return Response({
        "entries": social_action.entries,
        "msg": _('MSG_LIKE_TWITTER_VALIDATED'),
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def twitter_follow_validation(request):
    """
    This function permit to follow an twitter account
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.twitter_follow:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    if not user.social_connection.twitter_connected:
        return Response({
            "msg": _('MSG_ERROR_USER_NOT_CONNECTED_TO_TWITTER'),
            "status": 404
        }, status=404)
    try:
        social_action = UserSocialAction.objects.get(user=user, promotion=promotion)
    except UserSocialAction.DoesNotExist:
        social_action = UserSocialAction.objects.create(user=user, promotion=promotion)
    if social_action.twitter_follow:
        return Response({
            "msg": _('MSG_ERROR_ACTION_ALREADY_VALIDATED'),
            "status": 404
        }, status=404)
    try:
        api = twitter.Api(consumer_key=settings.TWITTER_API_KEY,
                          consumer_secret=settings.TWITTER_API_SECRET_KEY,
                          access_token_key=user.social_connection.twitter_oauth_token_data,
                          access_token_secret=user.social_connection.twitter_oauth_token_secret)
        if promotion.social_action.twitter_follow_type == 'user_id':
            api.CreateFriendship(user_id=promotion.social_action.twitter_follow_id)
        else:
            api.CreateFriendship(screen_name=promotion.social_action.twitter_follow_id)
    except Exception as e:
        return Response({
            "msg": _('MSG_ERROR_WITH_TWITTER_FOLLOW'),
            "status": 404
        }, status=404)
    social_action.twitter_follow = True
    social_action.entries = social_action.entries + promotion.social_action.entries.twitter_follow_entries
    social_action.save()
    try:
        analytics = PromotionNumbers.objects.filter(promotion=promotion).last()
        analytics.click_actions = analytics.click_actions + 1
        analytics.save()
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_WITH_ANALYTICS'),
            "status": 404
        }, status=404)
    return Response({
        "entries": social_action.entries,
        "msg": _('MSG_TWITTER_FOLLOW_VALIDATED'),
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def twitch_follow_validation(request):
    """
    This function permit to follow an twich account
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.twitch_follow:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    if not user.social_connection.twitch_connected:
        return Response({
            "msg": _('MSG_ERROR_USER_NOT_CONNECTED_TO_TWITCH'),
            "status": 404
        }, status=404)
    try:
        social_action = UserSocialAction.objects.get(user=user, promotion=promotion)
    except UserSocialAction.DoesNotExist:
        social_action = UserSocialAction.objects.create(user=user, promotion=promotion)
    if social_action.twitch_follow:
        return Response({
            "msg": _('MSG_ERROR_ACTION_ALREADY_VALIDATED'),
            "status": 404
        }, status=404)
    try:
        url = 'https://api.twitch.tv/kraken/search/channels?query=' + promotion.social_action.twitch_follow_name
        headers = {'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': settings.TWITCH_ID}
        r = requests.get(url, headers=headers)
        results = json.loads(r.text)
        results = results['channels']
        for result in results:
            if result['name'] == promotion.social_action.twitch_follow_name:
                try:
                    url = 'https://api.twitch.tv/kraken/users/' + user.social_connection.twitch_user_id \
                          + '/follows/channels/' + str(result['_id'])
                    headers = {'Accept': 'application/vnd.twitchtv.v5+json',
                               'Client-ID': settings.TWITCH_ID,
                               'Authorization': 'OAuth ' + user.social_connection.twitch_token}
                    r = requests.put(url, headers=headers)
                    social_action.twitch_follow = True
                    social_action.entries = social_action.entries + \
                                            promotion.social_action.entries.twitch_follow_entries
                    social_action.save()
                    try:
                        analytics = PromotionNumbers.objects.filter(promotion=promotion).last()
                        analytics.click_actions = analytics.click_actions + 1
                        analytics.save()
                    except Exception:
                        return Response({
                            "msg": _('MSG_ERROR_WITH_ANALYTICS'),
                            "status": 404
                        }, status=404)
                    return Response({
                        "entries": social_action.entries,
                        "msg": _('MSG_FOLLOW_VALIDATED'),
                        "status": 200
                    }, status=200)
                except Exception as e:
                    return Response({
                        "msg": _('MSG_ERROR_WITH_FOLLOW_TWITCH_ACCOUNT'),
                        "status": 404
                    }, status=404)
    except Exception as e:
        return Response({
            "msg": _('MSG_ERROR_WITH_FOLLOW_TWITCH_ACCOUNT'),
            "status": 404
        }, status=404)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def instagram_profile(request):
    """
    This function permit to visit an instagram publication
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.instagram_profile:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    try:
        social_action = UserSocialAction.objects.get(user=user, promotion=promotion)
    except UserSocialAction.DoesNotExist:
        social_action = UserSocialAction.objects.create(user=user, promotion=promotion)
    if social_action.instagram_profile:
        return Response({
            "msg": _('MSG_ERROR_ACTION_ALREADY_VALIDATED'),
            "status": 404
        }, status=404)
    social_action.instagram_profile = True
    social_action.entries = social_action.entries + promotion.social_action.entries.instagram_profile_entries
    social_action.save()
    try:
        analytics = PromotionNumbers.objects.filter(promotion=promotion).last()
        analytics.click_actions = analytics.click_actions + 1
        analytics.save()
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_WITH_ANALYTICS'),
            "status": 404
        }, status=404)
    return Response({
        "entries": social_action.entries,
        "msg": _('MSG_VALIDATED_PROFILE_INSTAGRAM'),
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def instagram_publication(request):
    """
    This function permit to visit an instagram publication
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.instagram_publication:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    try:
        social_action = UserSocialAction.objects.get(user=user, promotion=promotion)
    except UserSocialAction.DoesNotExist:
        social_action = UserSocialAction.objects.create(user=user, promotion=promotion)
    if social_action.instagram_publication:
        return Response({
            "msg": _('MSG_ERROR_ACTION_ALREADY_VALIDATED'),
            "status": 404
        }, status=404)
    social_action.instagram_publication = True
    social_action.entries = social_action.entries + promotion.social_action.entries.instagram_publication_entries
    social_action.save()
    try:
        analytics = PromotionNumbers.objects.filter(promotion=promotion).last()
        analytics.click_actions = analytics.click_actions + 1
        analytics.save()
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_WITH_ANALYTICS'),
            "status": 404
        }, status=404)
    return Response({
        "entries": social_action.entries,
        "msg": _('MSG_VALIDATED_PUBLICATION_INSTAGRAM'),
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def facebook_url(request):
    """
    This function permit to do the url publication with facebook
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
        action = request.data['action']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.facebook_url:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    if not user.social_connection.facebook_rights_connected:
        return Response({
            "msg": _('MSG_ERROR_USER_NOT_CONNECTED_TO_FACEBOOK'),
            "status": 404
        }, status=404)
    try:
        social_action = UserSocialAction.objects.get(user=user, promotion=promotion)
    except UserSocialAction.DoesNotExist:
        social_action = UserSocialAction.objects.create(user=user, promotion=promotion)
    if social_action.facebook_url:
        return Response({
            "msg": _('MSG_ERROR_ACTION_ALREADY_VALIDATED'),
            "status": 404
        }, status=404)
    social_action.facebook_url = True
    social_action.entries = social_action.entries + promotion.social_action.entries.facebook_url_entries
    social_action.save()
    try:
        analytics = PromotionNumbers.objects.filter(promotion=promotion).last()
        analytics.click_actions = analytics.click_actions + 1
        analytics.save()
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_WITH_ANALYTICS'),
            "status": 404
        }, status=404)
    return Response({
        "entries": social_action.entries,
        "msg": _('MSG_FACEBOOK_URL_VALIDATED'),
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def facebook_page(request):
    """
    Thins function permit to do actions on a page publication
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
        action = request.data['action']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.facebook_page:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    if not user.social_connection.facebook_rights_connected:
        return Response({
            "msg": _('MSG_ERROR_USER_NOT_CONNECTED_TO_FACEBOOK'),
            "status": 404
        }, status=404)
    try:
        social_action = UserSocialAction.objects.get(user=user, promotion=promotion)
    except UserSocialAction.DoesNotExist:
        social_action = UserSocialAction.objects.create(user=user, promotion=promotion)
    if social_action.facebook_page:
        return Response({
            "msg": _('MSG_ERROR_ACTION_ALREADY_VALIDATED'),
            "status": 404
        }, status=404)
    social_action.facebook_page = True
    social_action.entries = social_action.entries + promotion.social_action.entries.facebook_page_entries
    social_action.save()
    try:
        analytics = PromotionNumbers.objects.filter(promotion=promotion).last()
        analytics.click_actions = analytics.click_actions + 1
        analytics.save()
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_WITH_ANALYTICS'),
            "status": 404
        }, status=404)
    return Response({
        "entries": social_action.entries,
        "msg": _('MSG_FACEBOOK_PAGE_VALIDATED'),
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def facebook_post(request):
    """
    Thins function permit to do actions on a page publication
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
        action = request.data['action']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.facebook_post:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    if not user.social_connection.facebook_rights_connected:
        return Response({
            "msg": _('MSG_ERROR_USER_NOT_CONNECTED_TO_FACEBOOK'),
            "status": 404
        }, status=404)
    try:
        social_action = UserSocialAction.objects.get(user=user, promotion=promotion)
    except UserSocialAction.DoesNotExist:
        social_action = UserSocialAction.objects.create(user=user, promotion=promotion)
    if social_action.facebook_post:
        return Response({
            "msg": _('MSG_ERROR_ACTION_ALREADY_VALIDATED'),
            "status": 404
        }, status=404)
    social_action.facebook_post = True
    social_action.entries = social_action.entries + promotion.social_action.entries.facebook_post_entries
    social_action.save()
    try:
        analytics = PromotionNumbers.objects.filter(promotion=promotion).last()
        analytics.click_actions = analytics.click_actions + 1
        analytics.save()
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_WITH_ANALYTICS'),
            "status": 404
        }, status=404)
    return Response({
        "entries": social_action.entries,
        "msg": _('MSG_FACEBOOK_POST_VALIDATED'),
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def twitch_follow(request):
    """
    This function permit to follow an twitch account
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.twitch_follow:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    if not user.social_connection.twitch_connected:
        return Response({
            "msg": _('MSG_ERROR_USER_NOT_CONNECTED_TO_TWITCH'),
            "status": 404
        }, status=404)
    try:
        url = 'https://api.twitch.tv/kraken/search/channels?query=' + promotion.social_action.twitch_follow_name
        headers = {'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': settings.TWITCH_ID}
        r = requests.get(url, headers=headers)
        results = json.loads(r.text)
        results = results['channels']
        for result in results:
            if result['name'] == promotion.social_action.twitch_follow_name:
                url = 'https://api.twitch.tv/kraken/users/' + \
                      user.social_connection.twitch_user_id + '/follows/channels/' + str(result['_id'])
                headers = {'Accept': 'application/vnd.twitchtv.v5+json',
                           'Client-ID': settings.TWITCH_ID}
                r = requests.get(url, headers=headers)
                if r.status_code == 200:
                    try:
                        social_action = UserSocialAction.objects.get(user=user, promotion=promotion)
                        social_action.twitch_follow = True
                        social_action.save()
                    except UserSocialAction.DoesNotExist:
                        UserSocialAction.objects.create(user=user, promotion=promotion, twitch_follow=True)
                    return Response({
                        "msg": _('MSG_YOU_ARE_ALREADY_FOLLOWING_THIS_ACCOUNT'),
                        "status": 200,
                    }, status=200)
                return Response({
                    "msg": _('MSG_ACTION_EXIST'),
                    "name": result['display_name'],
                    "followers": result['followers'],
                    "profile_img": result['logo'],
                    "verified": result['partner'],
                    "status": 200
                }, status=200)
        return Response({
            "msg": _('MSG_ERROR_CHANNEL_NOT_FOUND'),
            "status": 404
        }, status=404)
    except Exception as e:
        return Response({
            "msg": _('MSG_ERROR_WITH_TWITCH_FOLLOW'),
            "status": 404
        }, status=404)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def twitter_follow(request):
    """
    This function permit to follow an twitter account
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.twitter_follow:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    if not user.social_connection.twitter_connected:
        return Response({
            "msg": _('MSG_ERROR_USER_NOT_CONNECTED_TO_TWITTER'),
            "status": 404
        }, status=404)
    try:
        result = None
        api = twitter.Api(consumer_key=settings.TWITTER_API_KEY,
                          consumer_secret=settings.TWITTER_API_SECRET_KEY,
                          access_token_key=user.social_connection.twitter_oauth_token_data,
                          access_token_secret=user.social_connection.twitter_oauth_token_secret)
        if promotion.social_action.twitter_follow_type == "user_id":
            result = api.GetUser(user_id=promotion.social_action.twitter_follow_id)
        elif promotion.social_action.twitter_follow_type == "screen_name":
            result = api.GetUser(screen_name=promotion.social_action.twitter_follow_id)
        if result and result.following:
            try:
                social_action = UserSocialAction.objects.get(user=user, promotion=promotion)
                social_action.twitter_follow = True
                social_action.save()
            except UserSocialAction.DoesNotExist:
                UserSocialAction.objects.create(user=user, promotion=promotion, twitter_follow=True)
            return Response({
                "msg": _('MSG_YOU_ARE_ALREADY_FOLLOWING_THIS_ACCOUNT'),
                "status": 200,
            }, status=200)
    except Exception as e:
        return Response({
            "msg": _('MSG_ERROR_WITH_TWITTER_FOLLOW'),
            "status": 404
        }, status=404)
    return Response({
        "msg": _('MSG_ACTION_EXIST'),
        "name": result.name,
        "followers": result.followers_count,
        "profile_img": result.profile_image_url_https,
        "verified": result.verified,
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def twitter_retweet_validation(request):
    """
    This function run the twitter retweet action
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.twitter_retweet:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    if not user.social_connection.twitter_connected:
        return Response({
            "msg": _('MSG_ERROR_USER_NOT_CONNECTED_TO_TWITTER'),
            "status": 404
        }, status=404)
    try:
        social_action = UserSocialAction.objects.get(user=user, promotion=promotion)
    except UserSocialAction.DoesNotExist:
        social_action = UserSocialAction.objects.create(user=user, promotion=promotion)
    if social_action.twitter_retweet:
        return Response({
            "msg": _('MSG_ERROR_ACTION_ALREADY_VALIDATED'),
            "status": 404
        }, status=404)
    try:
        api = twitter.Api(consumer_key=settings.TWITTER_API_KEY,
                          consumer_secret=settings.TWITTER_API_SECRET_KEY,
                          access_token_key=user.social_connection.twitter_oauth_token_data,
                          access_token_secret=user.social_connection.twitter_oauth_token_secret)
        api.PostRetweet(status_id=promotion.social_action.twitter_retweet_id)
    except Exception as e:
        return Response({
            "msg": _('MSG_ERROR_WITH_TWITTER_RETWEET'),
            "status": 404
        }, status=404)
    social_action.twitter_retweet = True
    social_action.entries = social_action.entries + promotion.social_action.entries.twitter_retweet_entries
    social_action.save()
    try:
        analytics = PromotionNumbers.objects.filter(promotion=promotion).last()
        analytics.click_actions = analytics.click_actions + 1
        analytics.save()
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_WITH_ANALYTICS'),
            "status": 404
        }, status=404)
    return Response({
        "entries": social_action.entries,
        "msg": _('MSG_TWITTER_RETWEET_VALIDATED'),
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def twitter_retweet(request):
    """
    This function run the twitter retweet action
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.twitter_retweet:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    if not user.social_connection.twitter_connected:
        return Response({
            "msg": _('MSG_ERROR_USER_NOT_CONNECTED_TO_TWITTER'),
            "status": 404
        }, status=404)
    try:
        api = twitter.Api(consumer_key=settings.TWITTER_API_KEY,
                          consumer_secret=settings.TWITTER_API_SECRET_KEY,
                          access_token_key=promotion.company.owner.social_connection.twitter_oauth_token_data,
                          access_token_secret=promotion.company.owner.social_connection.twitter_oauth_token_secret)
        retweet = api.GetStatus(status_id=promotion.social_action.twitter_retweet_id)
        if retweet.retweeted:
            try:
                social_action = UserSocialAction.objects.get(user=user, promotion=promotion)
                social_action.twitter_retweet = True
                social_action.save()
            except UserSocialAction.DoesNotExist:
                UserSocialAction.objects.create(user=user, promotion=promotion, twitter_retweet=True)
            return Response({
                "msg": _('MSG_YOU_HAVE_ALREADY_RETWEETED_THIS_TWEET'),
                "status": 200,
            }, status=200)
    except Exception as e:
        return Response({
            "msg": _('MSG_ERROR_WITH_TWITTER_TWEET'),
            "status": 404
        }, status=404)
    return Response({
        "msg": _('MSG_ACTION_EXIST'),
        "text": retweet.text,
        "like": retweet.favorite_count,
        "retweet": retweet.retweet_count,
        "created_at": retweet.created_at,
        "name": retweet.user.name,
        "verified": retweet.user.verified,
        "profile_img": retweet.user.profile_image_url_https,
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def twitter_tweet(request):
    """
    This function run the twitter tweet action
    :param request:
    :return:
    """
    try:
        promotion_pk = request.data['promotion_id']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    code, msg = verification_validation_action(user, promotion)
    if code != 200:
        return Response({
            "msg": _(msg),
            "status": code
        }, status=code)
    if not promotion.social_action.twitter_tweet:
        return Response({
            "msg": _('MSG_ACTION_NOT_ACTIVATED'),
            "status": 404
        }, status=404)
    if not user.social_connection.twitter_connected:
        return Response({
            "msg": _('MSG_ERROR_USER_NOT_CONNECTED_TO_TWITTER'),
            "status": 404
        }, status=404)
    return Response({
        "msg": _('MSG_ACTION_EXIST'),
        "tweet_template": promotion.social_action.twitter_tweet_model,
        "status": 200
    }, status=200)


def verification_mandatory(user_actions, entries):
    if entries.website_mandatory:
        if not user_actions.website:
            return False
    if entries.video_mandatory:
        if not user_actions.video:
            return False
    if entries.pool_mandatory:
        if not user_actions.poll:
            return False
    if entries.facebook_post_mandatory:
        if not user_actions.facebook_post:
            return False
    if entries.facebook_url_mandatory:
        if not user_actions.facebook_url:
            return False
    if entries.facebook_page_mandatory:
        if not user_actions.facebook_page:
            return False
    if entries.youtube_like_mandatory:
        if not user_actions.youtube_like:
            return False
    if entries.youtube_follow_mandatory:
        if not user_actions.youtube_follow:
            return False
    if entries.instagram_publication_mandatory:
        if not user_actions.instagram_publication:
            return False
    if entries.instagram_profile_mandatory:
        if not user_actions.instagram_profile:
            return False
    if entries.twitter_tweet_mandatory:
        if not user_actions.twitter_tweet:
            return False
    if entries.twitter_follow_mandatory:
        if not user_actions.twitter_follow:
            return False
    if entries.twitter_retweet_mandatory:
        if not user_actions.twitter_retweet:
            return False
    if entries.twitter_like_mandatory:
        if not user_actions.twitter_like:
            return False
    if entries.twitch_follow_mandatory:
        if not user_actions.twitch_follow:
            return False
    return True


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def participate(request):
    """
    This function permit to an user to participate to a promotion
    Args:
        request:
    Returns:
    """
    try:
        promotion_pk = request.data['promotion_id']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    if user.company_account:
        return Response({
            "msg": _('MSG_IMPOSSIBLE_TO_PARTICIPATE_WITH_PRO_ACCOUNT'),
            "status": 404
        }, status=404)
    if not user.phone_number_verification:
        return Response({
            "msg": _('MSG_PHONE_NUMBER_NOT_CONFIRMED'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    try:
        promotion.participants.get(pk=user.pk)
        return Response({
            "msg": _('MSG_ALREADY_PARTICIPATED'),
            "status": 404
        }, status=404)
    except ObjectDoesNotExist:
        pass
    try:
        user_actions = UserSocialAction.objects.get(user=user, promotion=promotion)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PARTICIPATION_NOT_VALIDATED'),
            "status": 404
        }, status=404)
    if verification_mandatory(user_actions, promotion.social_action.entries):
        promotion.participants.add(user)
        promotion.number_of_participants = promotion.number_of_participants + 1
        promotion.save()
        try:
            analytics = PromotionNumbers.objects.filter(promotion=promotion).last()
            analytics.click_participations = analytics.click_participations + 1
            analytics.save()
        except Exception:
            return Response({
                "msg": _('MSG_ERROR_WITH_ANALYTICS'),
                "status": 404
            }, status=404)
        return Response({
            "msg": _('MSG_PARTICIPATION_ACCEPTED'),
            "status": 200
        }, status=200)
    else:
        return Response({
            "msg": _('MSG_MANDATORY_ACTION_IS_NOT_VALIDATED'),
            "status": 400
        }, status=400)


def generation_coupon(winnings, start_date, promotion, people_eligible, type_of_distribution):
    """
    API endpoint for generating the differents coupon for the promotion
    Returns:
    """
    try:
        for winning in range(len(winnings)):
            winnings[winning]['number_of_people'] = int(winnings[winning]['number_of_people'])
        while people_eligible > 0:
            n = random.randint(0, len(winnings) - 1)
            if winnings[n]['number_of_people'] > 0:
                people_eligible = people_eligible - 1
                winnings[n]['number_of_people'] = winnings[n]['number_of_people'] - 1
                Coupon.objects.create(promotion=promotion, description=winnings[n]['description'],
                                      name=winnings[n]['name'], created=start_date,
                                      type_of_distribution=type_of_distribution)
            else:
                del winnings[n]
    except Exception:
        return False
    return True
