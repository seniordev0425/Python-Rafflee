"""
    Tools file for refresh token of the different social connection
"""

import json
import requests
import logging
from rafflee import settings

logger = logging.getLogger("django")


def refresh_twitch(user):
    try:
        if user.social_connection.twitch_connected_mobile:
            twitch_id = settings.TWITCH_ID_MOBILE
            twitch_secret = settings.TWITCH_MOBILE_SECRET_KEY
        else:
            twitch_id = settings.TWITCH_ID
            twitch_secret = settings.TWITCH_SECRET_KEY
        url = 'https://id.twitch.tv/oauth2/token'
        params = {
            "client_id": twitch_id,
            "client_secret": twitch_secret,
            "refresh_token": user.social_connection.twitch_refresh_token,
            "grant_type": "refresh_token"
        }
        response = requests.post(url, params=params)
        if response.status_code == 200:
            result = json.loads(response.text)
            user.social_connection.twitch_token = result['access_token']
            user.social_connection.twitch_refresh_token = result['refresh_token']
            user.save()
            return True
    except Exception as e:
        logger.debug("Error with the refresh token")
    return False
