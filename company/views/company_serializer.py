"""
    File with serialize function for company
"""

import os
import base64

from rest_framework import serializers
from tools.images import get_company_logo
from django.core.exceptions import ObjectDoesNotExist
from favorite.models import Subscription


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    """
        CompanySerializer class
    """

    def get_company_serializer(self, company):
        """
        This function serialize an company object
        :param company:
        :return:
        """
        user_data_json = dict()
        user_data_json['company_name'] = company.company_name
        user_data_json['logo'] = get_company_logo(company)
        return user_data_json

    def serialize_company(self, company, user):
        """
        This function serialize an company object
        Args:
            company: company object
            user: user object

        Returns:
            user_data: json object
        """
        user_data_json = dict()
        user_data_json['pk'] = company.pk
        try:
            subscription = Subscription.objects.get(user=user, company=company)
            user_data_json['follow'] = subscription.follow
            user_data_json['newsletter'] = subscription.newsletter
        except ObjectDoesNotExist:
            user_data_json['follow'] = None
            user_data_json['newsletter'] = None
        if user.phone_number is None:
            user_data_json['country_code'] = None
            user_data_json['national_number'] = None
        else:
            user_data_json['country_code'] = user.phone_number.country_code
            user_data_json['national_number'] = user.phone_number.national_number
        user_data_json['company_name'] = company.company_name
        user_data_json['twitter'] = user.social_connection.twitter_connected
        user_data_json['twitch'] = user.social_connection.twitch_connected
        user_data_json['instagram'] = user.social_connection.instagram_connected
        user_data_json['instagram_business'] = user.social_connection.facebook_page_connected
        user_data_json['facebook'] = user.social_connection.facebook_rights_connected
        user_data_json['logo'] = get_company_logo(company)
        user_data_json['address'] = company.address
        user_data_json['city'] = company.city
        user_data_json['country'] = company.country
        user_data_json['region'] = company.region
        user_data_json['email'] = user.email
        user_data_json['username'] = user.username
        return user_data_json

    def serialize_company_page(self, company, user=None):
        """
        This function serialize all the informations for the company page
        :param user:
        :param company:
        :return:
        """
        user_data_json = dict()
        user_data_json['pk'] = company.pk
        user_data_json['description'] = company.description
        user_data_json['company_name'] = company.company_name
        user_data_json['type_of_account'] = company.type_of_account
        user_data_json['logo_url'] = company.logo_url
        user_data_json['certified'] = company.certified
        if user:
            try:
                subscription = Subscription.objects.get(user=user, company=company)
                user_data_json['follow'] = subscription.follow
                user_data_json['newsletter'] = subscription.newsletter
            except ObjectDoesNotExist:
                user_data_json['follow'] = None
                user_data_json['newsletter'] = None
        else:
            user_data_json['follow'] = None
            user_data_json['newsletter'] = None
        try:
            user_data_json['website_url'] = company.social_network.website_url
        except:
            user_data_json['website_url'] = None
        try:
            user_data_json['youtube_channel'] = company.social_network.youtube_channel_url
        except:
            user_data_json['youtube_channel'] = None
        try:
            user_data_json['facebook_page_url'] = company.social_network.youtube_channel_url
        except:
            user_data_json['facebook_page_url'] = None
        try:
            user_data_json['twitter_page_url'] = company.social_network.youtube_channel_url
        except:
            user_data_json['twitter_page_url'] = None
        try:
            user_data_json['instagram_page_url'] = company.social_network.youtube_channel_url
        except:
            user_data_json['instagram_page_url'] = None
        try:
            user_data_json['number_of_follower'] = Subscription.objects.filter(company=company, follow=True).count()
        except:
            user_data_json['number_of_follower'] = 0
        user_data_json['member_since'] = company.created
        return user_data_json

    def _get_profile_logo(self, company):
        try:
            if not os.path.isfile(company.logo.file.name):
                return ''
        except Exception as e:
            return ''
        with open(company.logo.file.name, 'rb') as img_f:
            encoded_string = base64.b64encode(img_f.read())
        return encoded_string

