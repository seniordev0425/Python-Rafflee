"""
    Serializer object
"""

import logging
import os
import base64
from django.core.exceptions import ObjectDoesNotExist
from tools.images import get_company_logo, get_promotion_image, get_profil_picture, get_winning_picture
from rafflee import settings

logger = logging.getLogger("django")


def total_entries(obj, promotion):
    entries = 0
    if obj.facebook_url:
        entries = entries + promotion.social_action.entries.facebook_url_entries
    if obj.facebook_post:
        entries = entries + promotion.social_action.entries.facebook_post_entries
    if obj.facebook_page:
        entries = entries + promotion.social_action.entries.facebook_page_entries
    if obj.youtube_like:
        entries = entries + promotion.social_action.entries.youtube_like_entries
    if obj.youtube_follow:
        entries = entries + promotion.social_action.entries.youtube_follow_entries
    if obj.instagram_publication:
        entries = entries + promotion.social_action.entries.instagram_publication_entries
    if obj.instagram_profile:
        entries = entries + promotion.social_action.entries.instagram_profile_entries
    if obj.twitter_like:
        entries = entries + promotion.social_action.entries.twitter_like_entries
    if obj.twitter_tweet:
        entries = entries + promotion.social_action.entries.twitter_tweet_entries
    if obj.twitter_retweet:
        entries = entries + promotion.social_action.entries.twitter_retweet_entries
    if obj.twitter_follow:
        entries = entries + promotion.social_action.entries.twitter_follow_entries
    if obj.twitch_follow:
        entries = entries + promotion.social_action.entries.twitch_follow_entries
    if obj.poll:
        entries = entries + promotion.social_action.entries.pool_entries
    if obj.video:
        entries = entries + promotion.social_action.entries.video_entries
    if obj.website:
        entries = entries + promotion.social_action.entries.website_entries
    return entries

def set_user_actions(obj, promotion):
    """
    Set user social action for the serializer
    :param obj:
    :return:
    """
    return_all_actions = dict()
    return_all_actions['entries_user'] = total_entries(obj, promotion)
    return_all_actions['facebook_url'] = obj.facebook_url
    return_all_actions['facebook_post'] = obj.facebook_post
    return_all_actions['facebook_page'] = obj.facebook_page
    return_all_actions['youtube_like'] = obj.youtube_like
    return_all_actions['youtube_follow'] = obj.youtube_follow
    return_all_actions['instagram_publication'] = obj.instagram_publication
    return_all_actions['instagram_profile'] = obj.instagram_profile
    return_all_actions['twitter_like'] = obj.twitter_like
    return_all_actions['twitter_tweet'] = obj.twitter_tweet
    return_all_actions['twitter_retweet'] = obj.twitter_retweet
    return_all_actions['twitter_follow'] = obj.twitter_follow
    return_all_actions['twitch_follow'] = obj.twitch_follow
    return_all_actions['poll'] = obj.poll
    return_all_actions['video'] = obj.video
    return_all_actions['website'] = obj.website
    return return_all_actions

def set_social_actions(obj):
    """
    Set social action for the serializer
    Args:
        obj: promotion object
    Returns: dict
    """
    return_all_actions = dict()
    if obj.social_action.website:
        return_dict = dict()
        return_dict['url'] = obj.social_action.website_url
        return_dict['entries'] = obj.social_action.entries.website_entries
        return_dict['mandatory'] = obj.social_action.entries.website_mandatory
        return_all_actions['website'] = return_dict
    if obj.social_action.video:
        return_dict = dict()
        return_dict['url_video'] = obj.video.url
        return_dict['video_name'] = obj.video.video_name
        return_dict['entries'] = obj.social_action.entries.video_entries
        return_dict['mandatory'] = obj.social_action.entries.video_mandatory
        if obj.social_action.video_mobile:
            return_dict['url_video_mobile'] = obj.video.url_mobile
        else:
            return_dict['url_video_mobile'] = None
        return_all_actions['video'] = return_dict
    if obj.poll:
        return_dict = dict()
        responses = []
        try:
            for response in obj.poll.response.all():
                responses.append(response.response)
            return_dict['question'] = obj.poll.question.question
            return_dict['multiple_choices'] = obj.poll.multiple_choices
            return_dict['responses'] = responses
            return_dict['entries'] = obj.social_action.entries.pool_entries
            return_dict['mandatory'] = obj.social_action.entries.pool_mandatory
            return_all_actions['poll'] = return_dict
        except Exception as e:
            return_all_actions['poll'] = None
    else:
        return_all_actions['poll'] = None
    if obj.social_action:
        social = []
        fb_dict = dict()
        fb_dict['facebook_url'] = obj.social_action.facebook_url
        if obj.social_action.facebook_url:
            fb_dict['facebook_url_like'] = obj.social_action.facebook_url_like
            fb_dict['facebook_url_share'] = obj.social_action.facebook_url_share
            fb_dict['facebook_url_url'] = obj.social_action.facebook_url_url
            fb_dict['facebook_url_entries'] = obj.social_action.entries.facebook_url_entries
            fb_dict['facebook_url_mandatory'] = obj.social_action.entries.facebook_url_mandatory
        fb_dict['facebook_page'] = obj.social_action.facebook_page
        if obj.social_action.facebook_page:
            fb_dict['facebook_page_follow'] = obj.social_action.facebook_page_follow
            fb_dict['facebook_page_share'] = obj.social_action.facebook_page_share
            fb_dict['facebook_page_url'] = obj.social_action.facebook_page_url
            fb_dict['facebook_page_entries'] = obj.social_action.entries.facebook_page_entries
            fb_dict['facebook_page_mandatory'] = obj.social_action.entries.facebook_page_mandatory
        fb_dict['facebook_post'] = obj.social_action.facebook_post
        if obj.social_action.facebook_post:
            fb_dict['facebook_post_like'] = obj.social_action.facebook_post_like
            fb_dict['facebook_post_url'] = obj.social_action.facebook_post_url
            fb_dict['facebook_post_comment'] = obj.social_action.facebook_post_comment
            fb_dict['facebook_post_share'] = obj.social_action.facebook_post_share
            fb_dict['facebook_post_entries'] = obj.social_action.entries.facebook_post_entries
            fb_dict['facebook_post_mandatory'] = obj.social_action.entries.facebook_post_mandatory
        yt_dict = dict()
        yt_dict['youtube_like'] = obj.social_action.youtube_like
        yt_dict['youtube_follow'] = obj.social_action.youtube_follow
        yt_dict['youtube_like_entries'] = obj.social_action.entries.youtube_like_entries
        yt_dict['youtube_like_mandatory'] = obj.social_action.entries.youtube_like_mandatory
        yt_dict['youtube_follow_entries'] = obj.social_action.entries.youtube_follow_entries
        yt_dict['youtube_follow_mandatory'] = obj.social_action.entries.youtube_follow_mandatory
        instagram_dict = dict()
        instagram_dict['instagram_profile'] = obj.social_action.instagram_profile
        if obj.social_action.instagram_profile:
            instagram_dict['instagram_profile_url'] = obj.social_action.instagram_profile_url
            instagram_dict['instagram_profile_entries'] = obj.social_action.entries.instagram_profile_entries
            instagram_dict['instagram_profile_mandatory'] = obj.social_action.entries.instagram_profile_mandatory
        instagram_dict['instagram_publication'] = obj.social_action.instagram_publication
        if obj.social_action.instagram_publication:
            instagram_dict['instagram_publication_entries'] = obj.social_action.entries.instagram_publication_entries
            instagram_dict['instagram_publication_mandatory'] = \
                obj.social_action.entries.instagram_publication_mandatory
            instagram_dict['instagram_publication_url'] = obj.social_action.instagram_publication_url
        twitter_dict = dict()
        twitter_dict['twitter_like'] = obj.social_action.twitter_like
        twitter_dict['twitter_like_entries'] = obj.social_action.entries.twitter_like_entries
        twitter_dict['twitter_like_mandatory'] = obj.social_action.entries.twitter_like_mandatory
        twitter_dict['twitter_tweet'] = obj.social_action.twitter_tweet
        twitter_dict['twitter_tweet_entries'] = obj.social_action.entries.twitter_tweet_entries
        twitter_dict['twitter_tweet_mandatory'] = obj.social_action.entries.twitter_tweet_mandatory
        if obj.social_action.twitter_tweet:
            twitter_dict['twitter_tweet_model'] = obj.social_action.twitter_tweet_model
        twitter_dict['twitter_retweet'] = obj.social_action.twitter_retweet
        twitter_dict['twitter_retweet_entries'] = obj.social_action.entries.twitter_retweet_entries
        twitter_dict['twitter_retweet_mandatory'] = obj.social_action.entries.twitter_retweet_mandatory
        twitter_dict['twitter_follow'] = obj.social_action.twitter_follow
        twitter_dict['twitter_follow_entries'] = obj.social_action.entries.twitter_follow_entries
        twitter_dict['twitter_follow_mandatory'] = obj.social_action.entries.twitter_follow_mandatory
        twitch_dict = dict()
        twitch_dict['twitch_follow'] = obj.social_action.twitch_follow
        twitch_dict['twitch_follow_entries'] = obj.social_action.entries.twitch_follow_entries
        twitch_dict['twitch_follow_mandatory'] = obj.social_action.entries.twitch_follow_mandatory
        social.append(fb_dict)
        social.append(yt_dict)
        social.append(instagram_dict)
        social.append(twitter_dict)
        social.append(twitch_dict)
        return_all_actions['social_action'] = social
    else:
        return_all_actions['social_action'] = None
    return return_all_actions


def serialize_analytics_click_promotion(obj):
    """
    This function serialize an social numbers object
    :param obj:
    :return:
    """
    parsed_json = dict()
    parsed_json['click_views'] = obj.click_views
    parsed_json['click_actions'] = obj.click_actions
    parsed_json['click_participations'] = obj.click_participations
    parsed_json['date'] = obj.start_date
    return parsed_json


def serialize_analytics_click(obj):
    """
    This function serialize an analytics click object
    :param obj:
    :return:
    """
    parsed_json = dict()
    parsed_json['click_views'] = obj.click_views
    parsed_json['click_actions'] = obj.click_actions
    parsed_json['click_participations'] = obj.click_participations
    parsed_json['number_of_followers'] = obj.number_of_followers
    parsed_json['click_views_total'] = obj.click_views_total
    parsed_json['click_actions_total'] = obj.click_actions_total
    parsed_json['click_participations_total'] = obj.click_participations_total
    parsed_json['product_benefit_by_view'] = obj.product_benefit_by_view
    parsed_json['product_benefit_by_action'] = obj.product_benefit_by_action
    parsed_json['product_benefit_by_participations'] = obj.product_benefit_by_action
    parsed_json['product_benefit_by_total'] = obj.product_benefit_by_action
    parsed_json['product_benefit_followers'] = obj.product_benefit_followers
    parsed_json['date'] = obj.start_date
    return parsed_json


def serialize_analytics_social_numbers(obj):
    """
    This function serialize an social numbers object
    :param obj:
    :return:
    """
    parsed_json = dict()
    parsed_json['twitter'] = obj.twitter_followers
    parsed_json['rafflee'] = obj.rafflee_followers
    parsed_json['instagram'] = obj.instagram_followers
    parsed_json['facebook'] = obj.facebook_followers
    parsed_json['snapchat'] = obj.snapchat_followers
    parsed_json['twitch'] = obj.twitch_followers
    parsed_json['youtube'] = obj.youtube_followers
    parsed_json['date'] = obj.emission_date
    return parsed_json

def serialize_categorie_object(obj):
    """
    This function serialize an promotion object
    Args:
        obj: promotion object
    Returns: serializable object
    """
    parsed_json = dict()
    if obj.logo:
        parsed_json['logo'] = obj.logo
    parsed_json['name'] = obj.name
    parsed_json['description'] = obj.description
    return parsed_json


def serialize_dashboard_promotion_object(obj, analytics=None):
    """
    This function serialize an promotion object
    Args:
        obj: promotion object
    Returns: serializable object
    """
    parsed_json = dict()
    parsed_json['pk'] = obj.pk
    parsed_json['campaign_name'] = obj.campaign_name
    parsed_json['number_of_eligible_people'] = obj.number_of_eligible_people
    parsed_json['description'] = obj.description
    parsed_json['type_of_promotion'] = obj.type_of_promotion
    parsed_json['release_date'] = obj.release_date
    parsed_json['end_date'] = obj.end_date
    parsed_json['number_of_participants'] = obj.number_of_participants
    parsed_json['type_of_distribution'] = obj.type_of_distribution
    parsed_json['company_name'] = obj.company.company_name
    parsed_json['company_id'] = obj.company.pk
    parsed_json['live_draw'] = obj.live_draw
    parsed_json['close_promotion'] = obj.close_promotion
    parsed_json['nbr_of_views'] = analytics.click_views
    parsed_json['percentage_of_interest'] = analytics.product_benefit_by_total
    try:
        parsed_json['company_logo'] = get_company_logo(obj.company)
    except Exception as e:
        parsed_json['company_logo'] = None
    else:
        parsed_json['company_logo'] = None
    try:
        parsed_json['campaign_image'] = get_promotion_image(obj)
    except Exception as e:
        parsed_json['campaign_image'] = None
    try:
        winnings = obj.winnings.all()
        if winnings:
            parsed_json['winnings'] = []
            for winning in winnings:
                parsed_json['winnings'].append(winning.name)
        else:
            parsed_json['winnings'] = None
    except ObjectDoesNotExist:
        parsed_json['winnings'] = None
    try:
        categories = obj.categories.all()
        if categories:
            parsed_json['categories'] = []
            for category in categories:
                parsed_json['categories'].append(category.name)
        else:
            parsed_json['categories'] = None
    except ObjectDoesNotExist:
        parsed_json['categories'] = None
    if obj.poll or obj.social_action:
        parsed_json['action_participate'] = []
        parsed_json['action_participate'].append(set_social_actions(obj))
    else:
        parsed_json['action_participate'] = None
    return parsed_json


def serialize_promotion_object(obj, favorite=False, user_actions=None):
    """
    This function serialize an promotion object
    Args:
        favorite: If is is a favorite for the user
        obj: promotion object
    Returns: serializable object
    :param user_actions:
    """
    parsed_json = dict()
    parsed_json['pk'] = obj.pk
    parsed_json['company_id'] = obj.company.pk
    parsed_json['company_name'] = obj.company.company_name
    try:
        parsed_json['company_logo'] = get_company_logo(obj.company)
    except Exception as e:
        parsed_json['company_logo'] = None
    parsed_json['campaign_name'] = obj.campaign_name
    try:
        parsed_json['campaign_image'] = get_promotion_image(obj)
    except Exception as e:
        parsed_json['campaign_image'] = None
    parsed_json['number_of_eligible_people'] = obj.number_of_eligible_people
    parsed_json['description'] = obj.description
    parsed_json['long_description'] = obj.long_description
    parsed_json['type_of_distribution'] = obj.type_of_distribution
    parsed_json['release_date'] = obj.release_date
    parsed_json['end_date'] = obj.end_date
    parsed_json['close_promotion'] = obj.close_promotion
    parsed_json['live_draw'] = obj.live_draw
    try:
        winnings = obj.winnings.all()
        if winnings:
            parsed_json['winnings'] = []
            for winning in winnings:
                parsed_json['winnings'].append(winning.name)
        else:
            parsed_json['winnings'] = None
    except ObjectDoesNotExist:
        parsed_json['winnings'] = None
    try:
        categories = obj.categories.all()
        if categories:
            parsed_json['categories'] = []
            for category in categories:
                parsed_json['categories'].append(category.name)
        else:
            parsed_json['categories'] = None
    except ObjectDoesNotExist:
        parsed_json['categories'] = None
    if obj.poll or obj.social_action:
        parsed_json['action_participate'] = []
        parsed_json['action_participate'].append(set_social_actions(obj))
    else:
        parsed_json['action_participate'] = None
    if user_actions:
        parsed_json['user_actions'] = []
        parsed_json['user_actions'] = set_user_actions(user_actions, obj)
    else:
        parsed_json['user_actions'] = None
    parsed_json['favorite'] = favorite
    return parsed_json


def serialize_coupon_object(obj):
    """
    This function serialize an coupon object
    Args:
        obj: promotion object
    Returns: serializable object
    """
    parsed_json = dict()
    parsed_json['user'] = obj.user.username
    parsed_json['name'] = obj.name
    parsed_json['promotion'] = obj.promotion.campaign_name
    parsed_json['description'] = obj.description
    return parsed_json


def serialize_winning_object(obj, number):
    """
    This function serialize an coupon object
    Args:
        obj: promotion object
    Returns: serializable object
    """
    parsed_json = dict()
    parsed_json['name'] = obj.name
    parsed_json['number_of_eligible_people'] = obj.number_of_eligible_people
    if settings.SWIFT_USERFILES:
        parsed_json['image_url'] = obj.image_url
    else:
        try:
            parsed_json['winning_image'] = get_winning_picture(obj)
        except Exception:
            parsed_json['winning_image'] = None
    parsed_json['description'] = obj.description
    parsed_json['number_to_win'] = number
    return parsed_json


def serialize_winning_object_for_user(giveaway, promotion):
    """
    This function serialize an coupon object
    Args:
        obj: promotion object
    Returns: serializable object
    """
    parsed_json = dict()
    parsed_json['giveaway_name'] = giveaway.name
    parsed_json['number_of_eligible_people'] = giveaway.number_of_eligible_people
    if settings.SWIFT_USERFILES:
        parsed_json['giveaway_image_url'] = giveaway.image_url
    else:
        try:
            parsed_json['giveaway_image'] = get_winning_picture(giveaway)
        except Exception:
            parsed_json['giveaway_image'] = None
    parsed_json['giveaway_description'] = giveaway.description
    parsed_json['campaign_image'] = get_promotion_image(promotion)
    parsed_json['campaign_name'] = promotion.campaign_name
    parsed_json['campaign_description'] = promotion.description
    parsed_json['promotion_id'] = promotion.pk
    return parsed_json


def serialize_favorite_object(obj):
    """
    This function serialize an favorite object
    Args:
        obj: favorite object
    Returns: serializable object
    """
    parsed_json = dict()
    parsed_json['promotion'] = obj.promotion.campaign_name
    parsed_json['description'] = obj.promotion.description
    parsed_json['end_date'] = obj.promotion.end_date
    parsed_json['campaign_image'] = get_promotion_image(obj.promotion)
    parsed_json['company_image'] = get_company_logo(obj.promotion.company)
    parsed_json['promotion_id'] = obj.promotion.pk
    parsed_json['company_id'] = obj.promotion.company.pk
    return parsed_json


def serialize_favorite_company_object(obj):
    """
    This function serialize an favorite object
    Args:
        obj: favorite object
    Returns: serializable object
    """
    parsed_json = dict()
    parsed_json['id'] = obj.company.pk
    parsed_json['company_name'] = obj.company.company_name
    parsed_json['description'] = obj.company.description
    parsed_json['certified'] = obj.company.certified
    parsed_json['type_of_account'] = obj.company.type_of_account
    if settings.SWIFT_USERFILES:
        try:
            parsed_json['logo_url'] = obj.company.logo_url
        except Exception as e:
            parsed_json['logo_url'] = None
    return parsed_json


def serialize_bill_object(obj):
    """
    This function serialize an favorite object
    Args:
        obj: favorite object
    Returns: serializable object
    """
    parsed_json = dict()
    try:
        parsed_json['campaign_image'] = get_promotion_image(obj.promotion)
    except Exception:
        parsed_json['campaign_image'] = None
    parsed_json['promotion'] = obj.promotion.campaign_name
    parsed_json['id'] = obj.pk
    parsed_json['price'] = obj.price
    parsed_json['emission_date'] = obj.emission_date
    return parsed_json


def serialize_winner_object(obj):
    """
    This function serialize a winner object
    Args:
        obj: favorite object
    Returns: serializable object
    """
    parsed_json = dict()
    parsed_json['username'] = obj.user.username
    try:
        parsed_json['picture_profile'] = get_profil_picture(obj.user)
    except Exception as e:
        parsed_json['picture_profile'] = None
    parsed_json['winning'] = obj.name
    return parsed_json


def _get_profile_picture(user):
    """
    This function return the base64 of an image
    Args:
        user:

    Returns:

    """
    try:
        if not os.path.isfile(user.profile_picture.file.name):
            return ''
    except Exception as e:
        return ''
    encoded_string = ''
    with open(user.profile_picture.file.name, 'rb') as img_f:
        encoded_string = base64.b64encode(img_f.read())
    return encoded_string


def _get_promotion_image(promotion):
    """
    This function return the base64 of an image
    Args:
        user:

    Returns:

    """
    try:
        if not os.path.isfile(promotion.campaign_image.file.name):
            return ''
    except Exception as e:
        return ''
    encoded_string = ''
    with open(promotion.campaign_image.file.name, 'rb') as img_f:
        encoded_string = base64.b64encode(img_f.read())
    return encoded_string


def _get_company_image(company):
    """
    This function return the base64 of an image
    Args:
        user:

    Returns:

    """
    try:
        if not os.path.isfile(company.logo.file.name):
            return ''
    except Exception as e:
        return ''
    encoded_string = ''
    with open(company.logo.file.name, 'rb') as img_f:
        encoded_string = base64.b64encode(img_f.read())
    return encoded_string
