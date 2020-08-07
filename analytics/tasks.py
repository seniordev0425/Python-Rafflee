"""
    Cron job for analytics
"""

from __future__ import absolute_import, unicode_literals
import datetime
import requests
import logging
import twitter
import json
import re

from twitch import TwitchClient
from rafflee import settings
from analytics.models import SocialNumbers
from company.models import Company
from django.core.exceptions import ObjectDoesNotExist
from tools.refresh_token import refresh_twitch
from promotion.models import Promotion
from favorite.models import Subscription
from celery import shared_task
from django.utils import timezone
from promotion.views.finish_promotion import close_promotion
from .models.promotion_numbers import PromotionNumbers
from account.models import MyUser

from rest_framework.decorators import api_view

logger = logging.getLogger("django")


def instagram_followers(user):
    if user.social_connection.instagram_business_connected:
        url = 'https://graph.facebook.com/v7.0/' + user.social_connection.instagram_business_id
        params = {
            "access_token": user.social_connection.instagram_business_long_access_token,
            "fields": "followers_count",
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return json.loads(response.text)['follows_count']
        else:
            return 0
    elif user.social_connection.instagram_connected:
        try:
            user = user.social_connection.instagram_username
            url = 'https://www.instagram.com/' + user
            r = requests.get(url).text
            followers = re.search('"edge_followed_by":{"count":([0-9]+)}', r).group(1)
            return followers
        except Exception as e:
            return 0
    return 0


def facebook_followers(user):
    if user.social_connection.facebook_page_id is not None:
        url = 'https://graph.facebook.com/v7.0/' + user.social_connection.facebook_page_id
        params = {
            "access_token": user.social_connection.facebook_page_access_token,
            "fields": "fan_count",
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return json.loads(response.text)['fan_count']
        else:
            return 0
    return 0


def twitter_followers(user):
    if user.social_connection.twitter_connected:
        api = twitter.Api(consumer_key=settings.TWITTER_API_KEY,
                          consumer_secret=settings.TWITTER_API_SECRET_KEY,
                          access_token_key=user.social_connection.twitter_oauth_token_data,
                          access_token_secret=user.social_connection.twitter_oauth_token_secret)
        try:
            user_information = api.VerifyCredentials()
        except Exception as e:
            logger.debug("Token not valid")
            return 0
        return int(user_information.followers_count)
    return 0


def twitch_followers(user):
    if refresh_twitch(user):
        try:
            if user.social_connection.twitch_connected:
                if user.social_connection.twitch_connected_mobile:
                    client = TwitchClient(client_id=settings.TWITCH_ID_MOBILE,
                                          oauth_token=user.social_connection.twitch_token)
                else:
                    client = TwitchClient(client_id=settings.TWITCH_ID, oauth_token=user.social_connection.twitch_token)
                channel = client.channels.get()
                return channel['followers']
        except Exception as e:
            logger.debug("Token not valid")
            return 0
    return 0


def rafflee_followers(company):
    try:
        followers = Subscription.objects.filter(company=company, follow=True).count()
    except Exception:
        logger.debug("Error with circle followers")
        return 0
    return followers


@shared_task()
def check_social_followers():
    print('check social followers')
    try:
        companies = Company.objects.all()
    except ObjectDoesNotExist:
        logger.debug("No companies founded")
        return
    for company in companies:
        SocialNumbers.objects.create(company=company, twitter_followers=twitter_followers(company.owner),
                                     twitch_followers=twitch_followers(company.owner),
                                     rafflee_followers=rafflee_followers(company),
                                     instagram_followers=instagram_followers(company.owner),
                                     facebook_followers=facebook_followers(company.owner))


def count_benefit(today, yesterday, new):
    if yesterday.click_participations > 0:
        new.product_benefit_by_participations = ((today.click_participations -
                                                  yesterday.click_participations) /
                                                 yesterday.click_participations) * 100
    if yesterday.click_actions > 0:
        new.product_benefit_by_action = ((today.click_actions - yesterday.click_actions) /
                                         yesterday.click_actions) * 100
    if yesterday.click_views > 0:
        new.product_benefit_by_view = ((today.click_views - yesterday.click_views) /
                                       yesterday.click_views) * 100
    if (yesterday.click_views + yesterday.click_actions + yesterday.click_participations) > 0:
        new.product_benefit_by_total = (((today.click_views + today.click_actions +
                                          today.click_participations) -
                                         (yesterday.click_views + yesterday.click_actions +
                                          yesterday.click_participations)) /
                                        (yesterday.click_views + yesterday.click_actions +
                                         yesterday.click_participations)) * 100
    if yesterday.number_of_followers > 0:
        new.product_benefit_followers = ((today.number_of_followers - yesterday.number_of_followers) /
                                 yesterday.number_of_followers) * 100
    new.save()


def total_click(today, yesterday):
    if yesterday.click_views_total != 0:
        today.click_views_total = yesterday.click_views_total + today.click_views
    else:
        today.click_views_total = yesterday.click_views + today.click_views
    if yesterday.click_participations_total != 0:
        today.click_participations_total = yesterday.click_participations_total + today.click_participations
    else:
        today.click_participations_total = yesterday.click_participations + today.click_participations
    if yesterday.click_actions_total != 0:
        today.click_actions_total = yesterday.click_actions_total + today.click_actions
    else:
        today.click_actions_total = yesterday.click_actions + today.click_actions
    today.save()


@shared_task()
def creation_product_benefit_analytics():
    logger.warning("Enter on the creation benefit task")
    promotions = None
    today = None
    new_analytics = None
    try:
        promotions = Promotion.objects.all()
    except Exception:
        logger.warning("No promotion founded")
    if promotions:
        logger.warning("Promotion founded")
        for promotion in promotions:
            logger.warning("Analytics for promotion " + promotion.campaign_name)
            try:
                all_analytics = PromotionNumbers.objects.filter(promotion=promotion).order_by('-start_date')
                try:
                    today = all_analytics[0]
                    yesterday = all_analytics[1]
                    new_analytics = PromotionNumbers.objects.create(promotion=promotion)
                    count_benefit(today, yesterday, new_analytics)
                    total_click(today, yesterday)
                except:
                    if new_analytics is None:
                        new_analytics = PromotionNumbers.objects.create(promotion=promotion,
                                                                        click_views_total=today.click_views,
                                                                        click_participations_total=
                                                                        today.click_participations,
                                                                        click_actions_total = today.click_actions)
            except Exception as e:
                logger.warning("No promotion founded")


@shared_task()
def verification_if_the_promotion_is_finished():
    try:
        promotions = Promotion.objects.filter(close_promotion=False)
    except Exception:
        logger.debug("No promotion founded")
        return
    for promotion in promotions:
        if promotion.end_date < timezone.now():
            if not promotion.live_draw:
                pass
            close_promotion(promotion)


def renew_token_facebook(social_object):
    if social_object.facebook_rights_connected:
        if social_object.facebook_date_token < (datetime.date.today() - datetime.timedelta(days=1)):
            social_object.facebook_rights_connected = False
            social_object.save()


def renew_token_instagram(social_object):
    url = "https://graph.instagram.com/refresh_access_token"
    if social_object.instagram_business_connected:
        params = {'grant_type': 'ig_refresh_token', 'access_token': social_object.instagram_business_long_access_token}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            response = json.loads(response.text)
            social_object.instagram_business_long_access_token = response['access_token']
            social_object.instagram_business_date_token = datetime.date.today() + \
                                                          datetime.timedelta(seconds=response['expires_in'])
        social_object.save()
    elif social_object.instagram_connected:
        params = {'grant_type': 'ig_refresh_token', 'access_token': social_object.instagram_long_access_token}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            response = json.loads(response.text)
            social_object.instagram_business_long_access_token = response['access_token']
            social_object.instagram_business_date_token = datetime.date.today() + \
                                                          datetime.timedelta(seconds=response['expires_in'])
        social_object.save()


@shared_task()
def renew_token():
    try:
        all_users = MyUser.objects.all()
        try:
            for user in all_users:
                if user.social_connection:
                    if user.social_connection.facebook_rights_connected:
                        renew_token_facebook(user.social_connection)
                    if user.social_connection.instagram_business_connected or user.social_connection.instagram_connected:
                        renew_token_instagram(user.social_connection)
        except Exception as e:
            logger.debug("No social connection founded")
    except Exception as e:
        logger.debug("No user founded")
        return
    return None
