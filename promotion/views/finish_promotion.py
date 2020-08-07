"""
    Manage finish promotion views
"""

import logging
import random

from coupon.models import Coupon
from social_network.models.user_social_action import UserSocialAction


logger = logging.getLogger("django")


def count_nb_max_entries(promotion):
    return (promotion.social_action.entries.pool_entries + promotion.social_action.entries.website_entries +
            promotion.social_action.entries.video_entries +
            promotion.social_action.entries.instagram_profile_entries +
            promotion.social_action.entries.instagram_publication_entries +
            promotion.social_action.entries.facebook_post_entries +
            promotion.social_action.entries.facebook_url_entries +
            promotion.social_action.entries.facebook_page_entries +
            promotion.social_action.entries.youtube_like_entries +
            promotion.social_action.entries.youtube_follow_entries +
            promotion.social_action.entries.twitter_like_entries +
            promotion.social_action.entries.twitter_follow_entries +
            promotion.social_action.entries.twitter_retweet_entries +
            promotion.social_action.entries.twitter_tweet_entries +
            promotion.social_action.entries.twitch_follow_entries)


def draw_giveaway(promotion):
    nb_max_entries = count_nb_max_entries(promotion)
    if promotion.number_of_participants > promotion.number_of_eligible_people:
        null_prize = promotion.number_of_participants - promotion.number_of_eligible_people
        while null_prize > 0:
            Coupon.objects.create(promotion=promotion, description="You won nothing", created=promotion.created,
                                  type_of_distribution=promotion.type_of_distribution, name="You lost")
            null_prize = null_prize - 1
    while nb_max_entries > 0:
        participants = UserSocialAction.objects.filter(promotion=promotion, entries=nb_max_entries, distributed=False)
        while participants.count() > 0:
            participant = random.choice(participants)
            coupon = random.choice(Coupon.objects.filter(promotion=promotion, distributed=False))
            if not promotion.live_draw:
                coupon.visible = True
            coupon.distributed = True
            coupon.user = participant.user
            participant.distributed = True
            coupon.save()
            participant.save()
            participants = UserSocialAction.objects.filter(promotion=promotion,
                                                           entries=nb_max_entries, distributed=False)
        nb_max_entries = nb_max_entries - 1
    return True


def draw_reward(promotion):
    nb_max_entries = count_nb_max_entries(promotion)
    while nb_max_entries > 0:
        participants = UserSocialAction.objects.filter(promotion=promotion, entries=nb_max_entries, distributed=False)
        while participants.count() > 0:
            participant = random.choice(participants)
            coupon = random.choice(Coupon.objects.filter(promotion=promotion, distributed=False))
            if not promotion.live_draw:
                coupon.visible = True
            coupon.distributed = True
            coupon.user = participant.user
            participant.distributed = True
            coupon.save()
            participant.save()
            participants = UserSocialAction.objects.filter(promotion=promotion,
                                                           entries=nb_max_entries, distributed=False)
        nb_max_entries = nb_max_entries - 1
    return True


def close_promotion(promotion):
    promotion.close_promotion = True
    promotion.save()
    if promotion.type_of_distribution == "giveaway":
        draw_giveaway(promotion)
    elif promotion.type_of_distribution == "reward":
        draw_reward(promotion)
