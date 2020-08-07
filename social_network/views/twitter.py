"""
    Twitter tools
"""

import base64
import requests

from social_network.models import AccessToken
from django.core.exceptions import ObjectDoesNotExist
from rafflee import settings


def generate_token():
    token = ''
    try:
        obj = AccessToken.objects.last()
    except ObjectDoesNotExist:
        obj = AccessToken.objects.create()
    key_secret = '{}:{}'.format(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET_KEY).encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')
    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)
    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
    auth_data = {
        'grant_type': 'client_credentials'
    }
    try:
        auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    except Exception:
        return ''
    if auth_resp.status_code == 200:
        if not obj:
            obj = AccessToken.objects.create()
        obj.twitter_access_token = auth_resp.json()['access_token']
        obj.save()
        return obj.twitter_access_token
    else:
        return ''
