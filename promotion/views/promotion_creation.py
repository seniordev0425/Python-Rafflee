"""
    Manage promotion views
"""

import logging
import random
import json
import twitter
import facebook
import distutils
import requests

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.utils.dateparse import parse_date
from tools.json import ApiJsonResponse
from django.http import JsonResponse
from operator import itemgetter
from tools.file_request import document_in_request
from coupon.models import Coupon
from account.models import MyUser
from promotion.models import Promotion, Poll, Question, ResponseTemplate, Category, Video
from promotion.models import Winnings
from company.models import Company
from company.models import Bills
from coupon.views.participate_coupon import generation_coupon
from favorite.models import Subscription
from company.views.bills import create_bill_pdf
from tools.serializer import serialize_winning_object, serialize_winner_object
from social_network.models import SocialAction, Entries
from social_network.views.twitter import generate_token
from account.views.user_serializer import UserSerializer
from tools.images import store_campaign_picture, store_winnings_image
from analytics.models.promotion_numbers import PromotionNumbers
from rafflee import settings

logger = logging.getLogger("django")


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_winnings(request, pk):
    """
    This function permit to get all the information for winning object for a promotion
    Args:
        pk: pk of the promotion
        request:
    Returns:
    """
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    response = ApiJsonResponse()
    try:
        promotion = Promotion.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_NO_PROMOTION_FOUNDED'),
            "status": 404
        }, status=404)
    if promotion.company.owner == user:
        for winning in promotion.winnings.all():
            try:
                number = Coupon.objects.filter(promotion=promotion, name=winning.name, distributed=False).count()
            except ObjectDoesNotExist:
                return Response({
                    "msg": _('MSG_GIVEAWAY_NOT_EXIST'),
                    "status": 404
                }, status=404)
            response.set_multiples_data(serialize_winning_object(winning, number))
        response.set_result_code(200)
        response.set_result_msg("MSG_WINNER_FOUNDED")
    else:
        return Response({
            "msg": _('MSG_USER_IS_NOT_THE_OWNER'),
            "status": 404
        }, status=404)
    return JsonResponse(response.get_dict())


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_all_participants(request, pk):
    """
    This function permit to get all the participants to a promotion
    Args:
        pk: pk of the promotion
        request:
    Returns:
    """
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_NO_PROMOTION_FOUNDED'),
            "status": 404
        }, status=404)
    if promotion.company.owner == user:
        try:
            participants = promotion.participants.all()
        except ObjectDoesNotExist:
            return Response({
                "msg": _('MSG_GIVEAWAY_NOT_EXIST'),
                "status": 404
            }, status=404)
        all_participants = []
        user_serializer = UserSerializer()
        for participant in participants:
            all_participants.append(user_serializer.serialize_participant(participant))
        return Response({
            'participants': all_participants,
            'number_of_participants': promotion.number_of_participants,
            "status": 200,
            'msg': _('MSG_WINNERS_FOUNDED')
        }, status=200)
    else:
        return Response({
            "msg": _('MSG_USER_IS_NOT_THE_OWNER'),
            "status": 404
        }, status=404)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def live_draw(request, pk):
    """
    API endpoint for getting one winner from a promotion
    Args:
        pk:
        request:
    Returns:
    """
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_NO_PROMOTION_FOUNDED'),
            "status": 404
        }, status=404)
    if promotion.company.owner == user:
        if not promotion.close_promotion:
            return Response({
                "msg": _('MSG_PROMOTION_STILL_IN_PROGRESS'),
                "status": 404
            }, status=404)
        try:
            all_coupons = Coupon.objects.filter(promotion=promotion, distributed=True, visible=False)
        except ObjectDoesNotExist:
            return Response({
                "msg": _('MSG_ALL_WINNING_OBJECT_ARE_DISTRIBUTED'),
                "status": 404
            }, status=404)
        if not all_coupons:
            return Response({
                "msg": _('MSG_ALL_WINNING_OBJECT_ARE_DISTRIBUTED'),
                "status": 404
            }, status=404)
        n = random.randint(1, all_coupons.count())
        coupon = itemgetter(n - 1)(all_coupons)
        coupon.visible = True
        coupon.save()
        winner = serialize_winner_object(coupon)
        return Response({
            'winner': winner,
            'msg': _('MSG_WINNER_FOUNDED'),
            "status": 200
        }, status=200)
    return Response({
        "msg": _('MSG_USER_IS_NOT_THE_OWNER'),
        "status": 404
    }, status=404)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def live_draw_by_giveaway(request, pk):
    """
    API endpoint for getting all winner from a promotion by winning name
    Args:
        pk:
        request:
    Returns:
    """
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        winning_name = request.data['winning_name']
    except Exception:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_NO_PROMOTION_FOUNDED'),
            "status": 404
        }, status=404)
    if promotion.company.owner == user:
        if not promotion.close_promotion:
            return Response({
                "msg": _('MSG_PROMOTION_STILL_IN_PROGRESS'),
                "status": 404
            }, status=404)
        try:
            all_coupons = Coupon.objects.filter(promotion=promotion, name=winning_name, distributed=True, visible=False)
        except ObjectDoesNotExist:
            return Response({
                "msg": _('MSG_ALL_WINNING_OBJECT_ARE_DISTRIBUTED'),
                "status": 404
            }, status=404)
        if not all_coupons:
            return Response({
                "msg": _('MSG_ALL_WINNING_OBJECT_ARE_DISTRIBUTED'),
                "status": 404
            }, status=404)
        n = random.randint(1, all_coupons.count())
        coupon = itemgetter(n - 1)(all_coupons)
        coupon.visible = True
        coupon.save()
        winner = serialize_winner_object(coupon)
        return Response({
            'winner': winner,
            'msg': _('MSG_WINNER_FOUNDED'),
            "status": 200
        }, status=200)
    return Response({
        "msg": _('MSG_USER_IS_NOT_THE_OWNER'),
        "status": 404
    }, status=404)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def live_draw_all_by_giveaway(request, pk):
    """
    API endpoint for getting all the winners from a promotion by winning name
    Args:
        pk:
        request:
    Returns:
    """
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_NO_PROMOTION_FOUNDED'),
            "status": 404
        }, status=404)
    try:
        winning_name = request.data['winning_name']
    except Exception:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    if promotion.company.owner == user:
        if not promotion.close_promotion:
            return Response({
                "msg": _('MSG_PROMOTION_STILL_IN_PROGRESS'),
                "status": 404
            }, status=404)
        try:
            all_coupons = Coupon.objects.filter(promotion=promotion, distributed=True, name=winning_name, visible=False)
        except ObjectDoesNotExist:
            return Response({
                "msg": _('MSG_ALL_WINNING_OBJECT_ARE_DISTRIBUTED'),
                "status": 404
            }, status=404)
        if not all_coupons:
            return Response({
                "msg": _('MSG_ALL_WINNING_OBJECT_ARE_DISTRIBUTED'),
                "status": 404
            }, status=404)
        all_winners = []
        for coupon in all_coupons:
            coupon.visible = True
            coupon.save()
            all_winners.append(serialize_winner_object(coupon))
        return Response({
            'winners': all_winners,
            'msg': _('MSG_WINNER_FOUNDED'),
            "status": 200
        }, status=200)
    return Response({
        "msg": _('MSG_USER_IS_NOT_THE_OWNER'),
        "status": 404
    }, status=404)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def live_draw_all_finish(request, pk):
    """
    API endpoint for getting all the winners from a promotion
    Args:
        pk:
        request:
    Returns:
    """
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_NO_PROMOTION_FOUNDED'),
            "status": 404
        }, status=404)
    if promotion.company.owner == user:
        if not promotion.close_promotion:
            return Response({
                "msg": _('MSG_PROMOTION_STILL_IN_PROGRESS'),
                "status": 404
            }, status=404)
        try:
            all_coupons = Coupon.objects.filter(promotion=promotion, distributed=True, visible=False)
        except ObjectDoesNotExist:
            return Response({
                "msg": _('MSG_ALL_WINNING_OBJECT_ARE_DISTRIBUTED'),
                "status": 404
            }, status=404)
        if not all_coupons:
            return Response({
                "msg": _('MSG_ALL_WINNING_OBJECT_ARE_DISTRIBUTED'),
                "status": 404
            }, status=404)
        all_winners = []
        for coupon in all_coupons:
            coupon.visible = True
            coupon.save()
            all_winners.append(serialize_winner_object(coupon))
        return Response({
            "msg": _('MSG_WINNER_FOUNDED'),
            "winners": all_winners,
            "status": 200
        }, status=200)
    return Response({
        "msg": _('MSG_USER_IS_NOT_THE_OWNER'),
        "status": 404
    }, status=404)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def subscription_company_page(request, id):
    try:
        joign_cercle = bool(request.data['joign_cercle'])
        newsletter = bool(request.data['newsletter'])
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
        company = Company.objects.get(pk=id)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    try:
        subscription = Subscription.objects.get(user=user, company=company)
        subscription.follow = joign_cercle
        subscription.newsletter = newsletter
        subscription.save()
    except Exception:
        try:
            Subscription.objects.create(user=user, company=company, follow=joign_cercle,
                                        newsletter=newsletter)
        except Exception:
            return Response({
                "msg": _('MSG_SUBSCRIPTIONS_ERROR'),
                "status": 500
            }, status=500)
    return Response({
        "msg": _('MSG_SUBSCRIPTION_CREATED'),
        "status": 200
    }, status=200)


@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated,))
def settings_wall(request):
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        company = Company.objects.get(owner=user)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_COMPANY_NOT_EXIST'),
            "status": 404
        }, status=404)
    if request.method == 'POST':
        try:
            twitter = json.loads(request.data['twitter'])
            facebook = json.loads(request.data['facebook'])
            instagram = json.loads(request.data['instagram'])
        except Exception as e:
            return Response({
                "msg": _('MSG_ERROR_FIELD: ' + e.args[0]),
                "status": 404
            }, status=404)
        try:
            company.owner.settings_wall.twitter = twitter
            company.owner.settings_wall.instagram = instagram
            company.owner.settings_wall.facebook = facebook['activate']
            company.owner.settings_wall.id_page_facebook = facebook['id']
            company.owner.settings_wall.save()
            return Response({
                "msg": _('MSG_WALL_SETTINGS_UPDATED'),
                "status": 200
            }, status=200)
        except Exception as e:
            return Response({
                "msg": _('MSG_ERROR_WITH_WALL_SETTINGS'),
                "status": 500
            }, status=500)
    if request.method == 'GET':
        return Response({
            "msg": _('MSG_WALL_SETTINGS_RETURNED'),
            "twitter": company.owner.settings_wall.twitter,
            "instagram": company.owner.settings_wall.instagram,
            "facebook": {"id": company.owner.settings_wall.id_page_facebook,
                         "activate": company.owner.settings_wall.facebook},
            "status": 200
        }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def unfollow_company_page(request, id):
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        company = Company.objects.get(pk=id)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    try:
        subscription = Subscription.objects.get(user=user, company=company)
        subscription.follow = False
        subscription.save()
    except Exception:
        try:
            Subscription.objects.create(user=user, company=company, follow=False)
        except Exception:
            return Response({
                "msg": _('MSG_UNFOLLOW_ERROR'),
                "status": 500
            }, status=500)
    return Response({
        "msg": _('MSG_UNFOLLOW_CIRCLE'),
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def subscription(request, id):
    try:
        joign_cercle = bool(request.data['joign_cercle'])
        newsletter = bool(request.data['newsletter'])
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
        promotion = Promotion.objects.get(pk=id)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    try:
        subscription = Subscription.objects.get(user=user, company=promotion.company)
        subscription.follow = joign_cercle
        subscription.newsletter = newsletter
    except Exception:
        try:
            Subscription.objects.create(user=user, company=promotion.company, follow=joign_cercle,
                                        newsletter=newsletter)
        except Exception:
            return Response({
                "msg": _('MSG_SUBSCRIPTIONS_ERROR'),
                "status": 500
            }, status=500)
    return Response({
        "msg": _('MSG_SUBSCRIPTION_UPDATED'),
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_promotion(request):
    """
    This function permit to create a promotion
    Args:
        request:
    Returns:
    """
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        campaign_name = request.data['promotion_name']
        promotion_description = request.data['promotion_description']
        promotion_long_description = request.data['promotion_long_description']
        winnings = json.loads(request.data['winnings'])
        campaign_picture = document_in_request('promotion_picture', request.FILES)
        poll = json.loads(request.data['poll'])
        facebook = json.loads(request.data['facebook'])
        categories = json.loads(request.data['categories'])
        twitter = json.loads(request.data['twitter'])
        instagram = json.loads(request.data['instagram'])
        youtube = json.loads(request.data['youtube'])
        twitch = json.loads(request.data['twitch'])
        campaign_type = request.data['promotion_type']
        campaign_option = json.loads(request.data['promotion_option'])
        campaign_public = request.data['public_promotion']
        start_date = parse_date(request.data['start_date'])
        url_video = json.loads(request.data['url_video'])
        url_website = json.loads(request.data['url_website'])
        end_date = parse_date(request.data['end_date'])
    except Exception as e:
        return Response({
            "msg": _('MSG_ERROR_FIELD: ' + e.args[0]),
            "status": 404
        }, status=404)
    try:
        company = Company.objects.get(owner=user)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_COMPANY_NOT_EXIST'),
            "status": 404
        }, status=404)
    # HERE DEFINITION OF THE PRICE
    price = 100
    try:
        entries = Entries.objects.create()
        social_action = SocialAction.objects.create(campaign_name=campaign_name, company_name=company.company_name,
                                                    entries=entries)
        for action in facebook:
            if action['action'] == "post":
                social_action.facebook_post = True
                social_action.entries.facebook_post_entries = action['entries']
                social_action.entries.facebook_post_mandatory = action['mandatory']
                social_action.facebook_post_url = action['url']
                social_action.facebook_post_like = action['like']
                social_action.facebook_post_comment = action['comment']
                social_action.facebook_post_share = action['share']
            elif action['action'] == "url":
                social_action.facebook_url = True
                social_action.entries.facebook_url_entries = action['entries']
                social_action.entries.facebook_url_mandatory = action['mandatory']
                social_action.facebook_url_url = action['url']
                social_action.facebook_url_like = action['like']
                social_action.facebook_url_share = action['share']
            elif action['action'] == "page":
                social_action.facebook_page = True
                social_action.entries.facebook_page_entries = action['entries']
                social_action.entries.facebook_page_mandatory = action['mandatory']
                social_action.facebook_page_follow = action['follow']
                social_action.facebook_page_share = action['share']
                social_action.facebook_page_url = action['url']
        for action in youtube:
            if action['action'] == "like":
                social_action.youtube_like = True
                social_action.entries.youtube_like_entries = action['entries']
                social_action.entries.youtube_like_mandatory = action['mandatory']
            elif action['action'] == "follow":
                social_action.youtube_follow = True
                social_action.entries.youtube_follow_entries = action['entries']
                social_action.entries.youtube_follow_mandatory = action['mandatory']
        for action in instagram:
            if action['action'] == "instagram_profile":
                social_action.instagram_profile = True
                social_action.instagram_profile_url = action['url']
                social_action.entries.instagram_profile_entries = action['entries']
                social_action.entries.instagram_profile_mandatory = action['mandatory']
            elif action['action'] == "instagram_publication":
                social_action.instagram_publication = True
                social_action.instagram_publication_url = action['url']
                social_action.entries.instagram_publication_entries = action['entries']
                social_action.entries.instagram_publication_mandatory = action['mandatory']
        for action in twitch:
            if action['action'] == "follow":
                social_action.twitch_follow = True
                social_action.twitch_follow_name = action['follow_name']
                social_action.entries.twitch_follow_entries = action['entries']
                social_action.entries.twitch_follow_mandatory = action['mandatory']
        for action in twitter:
            if action['action'] == "like":
                social_action.twitter_like = True
                social_action.twitter_like_id = action['id']
                social_action.entries.twitter_like_entries = action['entries']
                social_action.entries.twitter_like_mandatory = action['mandatory']
            elif action['action'] == "retweet":
                social_action.twitter_retweet = True
                social_action.twitter_retweet_id = action['id']
                social_action.entries.twitter_retweet_entries = action['entries']
                social_action.entries.twitter_retweet_mandatory = action['mandatory']
            elif action['action'] == "follow":
                social_action.twitter_follow = True
                social_action.twitter_follow_id = action['id']
                social_action.twitter_follow_type = action['type']
                social_action.entries.twitter_follow_entries = action['entries']
                social_action.entries.twitter_follow_mandatory = action['mandatory']
            elif action['action'] == "tweet":
                social_action.twitter_tweet_model = action['model']
                social_action.twitter_tweet = True
                social_action.entries.twitter_tweet_entries = action['entries']
                social_action.entries.twitter_tweet_mandatory = action['mandatory']
        social_action.entries.save()
        social_action.save()
    except Exception as e:
        return Response({
            "msg": _('MSG_NO_SOCIAL_ACTION_FOUNDED'),
            "status": 500
        }, status=500)
    try:
        promotion = Promotion.objects.create(campaign_name=campaign_name, company=company,
                                             description=promotion_description, type_of_promotion=campaign_public,
                                             release_date=start_date, end_date=end_date,
                                             type_of_distribution=campaign_type, social_action=social_action,
                                             long_description=promotion_long_description)
        bill = Bills.objects.create(company=company, promotion=promotion, price=price)
        if campaign_picture:
            store_campaign_picture(campaign_picture, promotion)
        create_bill_pdf(bill)
    except Exception as e:
        return Response({
            "msg": _('MSG_ERROR_SERVER_PROMOTION_CREATION'),
            "status": 500
        }, status=500)
    if categories:
        try:
            for category in categories:
                promotion.categories.add(Category.objects.get(name=category['name']))
        except Exception as e:
            promotion.delete()
            return Response({
                "msg": _('MSG_ERROR_SERVER_CATEGORIES_CREATION'),
                "status": 500
            }, status=500)
    if url_website:
        try:
            social_action.website = True
            social_action.entries.website_entries = url_website['entries']
            social_action.website_url = url_website['url']
            social_action.entries.website_mandatory = url_website['mandatory']
            social_action.save()
            social_action.entries.save()
            promotion.save()
        except Exception as e:
            promotion.delete()
            return Response({
                "msg": _('MSG_ERROR_SERVER_CREATION_URL_WEBSITE'),
                "status": 500
            }, status=500)
    if url_video:
        try:
            social_action.video = True
            social_action.entries.video_entries = url_video['entries']
            social_action.entries.video_mandatory = url_video['mandatory']
            if url_video['url_mobile'] is not "":
                social_action.video_mobile = True
                promotion.video = Video.objects.create(video_name=url_video['video_name'], url=url_video['url'],
                                                       url_mobile=url_video['url_mobile'])
            else:
                promotion.video = Video.objects.create(video_name=url_video['video_name'], url=url_video['url'])
            social_action.entries.save()
            social_action.save()
            promotion.save()
        except Exception as e:
            promotion.delete()
            return Response({
                "msg": _('MSG_ERROR_SERVER_CREATION_URL_VIDEO'),
                "status": 500
            }, status=500)
    if poll:
        try:
            social_action.poll = True
            social_action.entries.pool_entries = poll['entries']
            social_action.entries.pool_mandatory = poll['mandatory']
            new_poll = Poll.objects.create(multiple_choices=poll['mutiples_choices'],
                                           question=Question.objects.create(question=poll['question']))
            for response in poll['response']:
                new_poll.response.add(ResponseTemplate.objects.create(response=response))
                new_poll.save()
            promotion.poll = new_poll
            social_action.entries.save()
            social_action.save()
            promotion.save()
        except Exception as e:
            promotion.delete()
            return Response({
                "msg": _('MSG_ERROR_SERVER_CREATION_POLL'),
                "status": 500
            }, status=500)
    total_number_of_people = 0
    for winning in winnings:
        try:
            total_number_of_people = total_number_of_people + int(winning['number_of_people'])
            new_winning = Winnings.objects.create(name=winning['name'],
                                                  number_of_eligible_people=int(winning['number_of_people']),
                                                  description=winning['description'])
            promotion.winnings.add(new_winning)
            try:
                if winning['image']:
                    store_winnings_image(winning['image'], new_winning)
            except Exception as e:
                logger.debug("Error with the image of the winning object")
        except Exception as e:
            promotion.delete()
            return Response({
                "msg": _('MSG_ERROR_SERVER_GIVEAWAY_CREATION'),
                "status": 500
            }, status=500)
    promotion.number_of_eligible_people = total_number_of_people
    if campaign_type == "reward":
        promotion.number_of_maximum_participants = total_number_of_people
    elif campaign_type == "giveaway":
        try:
            if campaign_option['limitation_participation'] and campaign_option['limitation_participation'] > 0:
                promotion.number_of_maximum_participants = campaign_option['limitation_participation']
        except Exception as e:
            pass
    try:
        if campaign_option['live_draw']:
            promotion.live_draw = campaign_option['live_draw']
    except Exception as e:
        pass
    promotion.save()
    try:
        PromotionNumbers.objects.create(promotion=promotion)
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_ANALYTICS_CREATION'),
            "status": 500
        }, status=500)
    if generation_coupon(winnings, start_date, promotion, total_number_of_people, campaign_type):
        return Response({
            "msg": _('MSG_PROMOTION_CREATED'),
            "promotion_id": promotion.pk,
            "status": 200
        }, status=200)
    else:
        promotion.delete()
        return Response({
            "msg": _('MSG_ERROR_SERVER_COUPON_CREATION'),
            "status": 500
        }, status=500)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def twitter_search_users(request):
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        search = request.GET.get('search', '')
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    if user.company_account:
        try:
            api = twitter.Api(consumer_key=settings.TWITTER_API_KEY,
                              consumer_secret=settings.TWITTER_API_SECRET_KEY,
                              access_token_key=settings.TWITTER_ACCESS_TOKEN,
                              access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET)
            result = api.GetUsersSearch(term=search, count=10)
            ret = []
            for user in result:
                ret.append({'profile_image_url': user.profile_image_url_https, 'followers_count': user.followers_count,
                            'screen_name': user.screen_name, 'verified': user.verified})
            return Response({
                "search": ret,
                "msg": _('MSG_TWITTER_USER_RETURNED'),
                "status": 200
            }, status=200)
        except Exception as e:
            return Response({
                "msg": _('MSG_ERROR_TWITTER_SEARCH'),
                "status": 500
            }, status=500)
    else:
        return Response({
            "msg": _('MSG_ERROR_COMPANY_ACCOUNT'),
            "status": 404
        }, status=404)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def facebook_search_publication(request):
    try:
        id = request.data['page_id']
        access_token_page = request.data['page_access_token']
    except Exception as e:
        return Response({
            "msg": _('MSG_ERROR_FIELD: ' + e.args[0]),
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
        if user.social_connection.facebook_rights_connected:
            user.social_connection.facebook_page_access_token = access_token_page
            user.social_connection.facebook_page_connected = True
            user.social_connection.facebook_page_id = id
            user.social_connection.save()
            try:
                url = "https://graph.facebook.com/" + user.social_connection.facebook_page_id + "/feed"
                params = {
                    "access_token": user.social_connection.facebook_page_access_token,
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    response = json.loads(response.text)
                    ret = []
                    for elem in response['data']:
                        ret.append(elem)
                    return Response({
                        "search": ret,
                        "msg": _('MSG_FACEBOOK_PUBLICATION_RETURNED'),
                        "status": 200
                    }, status=200)
                else:
                    return Response({
                        "msg": _('MSG_ERROR_NO_FACEBOOK_PUBLICATION'),
                        "status": 404
                    }, status=404)
            except Exception as e:
                return Response({
                    "msg": _('MSG_ERROR_FACEBOOK_SEARCH_PUBLICATION'),
                    "status": 500
                }, status=500)
        else:
            return Response({
                "msg": _('MSG_ERROR_FACEBOOK_NOT_CONNECTED'),
                "status": 404
            }, status=404)
    else:
        return Response({
            "msg": _('MSG_ERROR_COMPANY_ACCOUNT'),
            "status": 404
        }, status=404)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def facebook_search_page(request):
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    if user.company_account:
        if user.social_connection.facebook_rights_connected:
            try:
                url = "https://graph.facebook.com/" + user.social_connection.facebook_id + "/accounts"
                params = {
                    "access_token": user.social_connection.facebook_long_access_token
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    response = json.loads(response.text)
                    ret = []
                    for elem in response['data']:
                        obj = {'name': elem['name'], 'access_token': elem['access_token'], 'id': elem['id']}
                        ret.append(obj)
                    return Response({
                        "search": ret,
                        "msg": _('MSG_FACEBOOK_PAGE_RETURNED'),
                        "status": 200
                    }, status=200)
                else:
                    return Response({
                        "msg": _('MSG_ERROR_NO_FACEBOOK_PUBLICATION'),
                        "status": 404
                    }, status=404)
            except Exception as e:
                return Response({
                    "msg": _('MSG_ERROR_FACEBOOK_SEARCH_PUBLICATION'),
                    "status": 500
                }, status=500)
        else:
            return Response({
                "msg": _('MSG_ERROR_FACEBOOK_NOT_CONNECTED'),
                "status": 404
            }, status=404)
    else:
        return Response({
            "msg": _('MSG_ERROR_COMPANY_ACCOUNT'),
            "status": 404
        }, status=404)
