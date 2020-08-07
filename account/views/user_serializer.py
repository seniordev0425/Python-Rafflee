"""
    File with serialize function for users
"""

import os
import base64

from rest_framework import serializers
from tools.images import get_profil_picture


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
        UserSerializer class
    """

    def serialize_users(self, user):
        """
        This function serialize an user object
        Args:
            user: user object

        Returns:
            user_data: json object
        """
        user_data_json = dict()
        if user.date_of_birth is None:
            user_data_json['birth_date'] = None
        else:
            user_data_json['birth_date'] = user.date_of_birth.isoformat()
        if user.phone_number is None:
            user_data_json['country_code'] = None
            user_data_json['national_number'] = None
        else:
            user_data_json['country_code'] = user.phone_number.country_code
            user_data_json['national_number'] = user.phone_number.national_number
        user_data_json['phone_number_verification'] = user.phone_number_verification
        try:
            user_data_json['profile_picture'] = get_profil_picture(user)
        except Exception as e:
            user_data_json['profile_picture'] = None
        user_data_json['twitter'] = user.social_connection.twitter_connected
        user_data_json['twitch'] = user.social_connection.twitch_connected
        user_data_json['instagram'] = user.social_connection.instagram_connected
        user_data_json['facebook'] = user.social_connection.facebook_rights_connected
        if user.address is None:
            user_data_json['address'] = None
        else:
            user_data_json['address'] = user.address
        if user.city is None:
            user_data_json['city'] = None
        else:
            user_data_json['city'] = user.city
        if user.country is None:
            user_data_json['country'] = None
        else:
            user_data_json['country'] = user.country
        if user.region is None:
            user_data_json['region'] = None
        else:
            user_data_json['region'] = user.region
        if user.first_name is None:
            user_data_json['firstname'] = None
        else:
            user_data_json['firstname'] = user.first_name
        if user.last_name is None:
            user_data_json['lastname'] = None
        else:
            user_data_json['lastname'] = user.last_name
        if user.username is None:
            user_data_json['username'] = None
        else:
            user_data_json['username'] = user.username
        if user.email is None:
            user_data_json['email'] = None
        else:
            user_data_json['email'] = user.email
        if user.gender is None:
            user_data_json['gender'] = None
        else:
            user_data_json['gender'] = user.gender
        return user_data_json


    def serialize_participant(self, user):
        """
        This function serialize an participant object
        Args:
            user: user object

        Returns:
            user_data: json object
        """
        user_data_json = dict()
        user_data_json['username'] = user.username
        user_data_json['email'] = user.email
        return user_data_json

    def _get_profile_picture(self, user):
        try:
            if not os.path.isfile(user.profile_picture.file.name):
                return ''
        except Exception as e:
            return ''
        encoded_string = ''
        with open(user.profile_picture.file.name, 'rb') as img_f:
            encoded_string = base64.b64encode(img_f.read())
        return encoded_string
