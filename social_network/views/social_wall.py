"""
    Social algorithm views
"""

import twitter
import requests
import json
import datetime

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from account.models import MyUser
from company.models import Company
from rafflee import settings


def twitter_wall(user):
    twitter_dict = {}
    if user.settings_wall.twitter:
        if user.social_connection.twitter_connected:
            api = twitter.Api(consumer_key=settings.TWITTER_API_KEY,
                              consumer_secret=settings.TWITTER_API_SECRET_KEY,
                              access_token_key=user.social_connection.twitter_oauth_token_data,
                              access_token_secret=user.social_connection.twitter_oauth_token_secret)
            try:
                user_information = api.VerifyCredentials()
                tweets = api.GetUserTimeline(screen_name=user_information.screen_name)
                try:
                    twitter_dict['friends'] = user_information.friends_count
                    twitter_dict['followers'] = user_information.followers_count
                    twitter_dict['name'] = user_information.name
                    twitter_dict['profile_image_url'] = user_information.profile_image_url_https
                    twitter_dict['verified'] = user_information.verified
                    twitter_dict['tweets'] = []
                    for s in tweets:
                        twitter_timeline = {'text': s.text, 'retweeted': s.retweeted, 'created_at': s.created_at}
                        twitter_dict['tweets'].append(twitter_timeline)
                    twitter_dict['error'] = False
                except Exception as e:
                    twitter_dict['error'] = True
            except Exception as e:
                twitter_dict['error'] = True
        else:
            return None
        return twitter_dict
    return False


def instagram_wall(user):
    instagram_dict = {}
    if user.settings_wall.instagram:
        if user.social_connection.instagram_connected:
            try:
                url = "https://graph.instagram.com/" + str(user.social_connection.instagram_id) + "/media"
                params = {"access_token": user.social_connection.instagram_long_access_token}
                response = requests.get(url, params=params)
                list = json.loads(response.content.decode('utf-8'))
                instagram_dict['publication'] = []
                for elem in list['data']:
                    url = "https://graph.instagram.com/" + str(elem['id'])
                    params = {
                        "access_token": user.social_connection.instagram_long_access_token,
                        "fields": "caption,permalink,timestamp,username,media_url,media_type"
                    }
                    response = requests.get(url, params=params)
                    response = json.loads(response.text)
                    if not 'name' in instagram_dict:
                        instagram_dict['name'] = response['username']
                    instagram_timeline = {'text': response['caption'], 'permalink': response['permalink'],
                                          'created_at': str(datetime.datetime.strptime(response['timestamp'],
                                                                                "%Y-%m-%dT%H:%M:%S+%f").ctime()),
                                          'media_url': response['media_url'],
                                          'media_type': response['media_type']}
                    instagram_dict['publication'].append(instagram_timeline)
                instagram_dict['error'] = False
            except Exception as e:
                instagram_dict['error'] = True
        else:
            return None
        return instagram_dict
    return False


def facebook_wall(user):
    facebook_dict = {}
    if user.settings_wall.facebook:
        if user.settings_wall.id_page_facebook is not "":
            if user.social_connection.facebook_rights_connected:
                try:
                    url = "https://graph.facebook.com/" + user.settings_wall.id_page_facebook
                    params = {
                        "access_token": user.social_connection.facebook_page_access_token,
                        "fields": "fan_count,link,website,picture{url},verification_status,name"
                    }
                    response = requests.get(url, params=params)
                    if response.status_code == 200:
                        facebook_dict['page_informations'] = json.loads(response.text)
                except Exception as e:
                    facebook_dict['error'] = True
                try:
                    url = "https://graph.facebook.com/" + user.settings_wall.id_page_facebook + "/feed"
                    params = {
                        "access_token": user.social_connection.facebook_page_access_token,
                        "fields": "picture,story,permalink_url,message,created_time",
                    }
                    response = requests.get(url, params=params)
                    if response.status_code == 200:
                        response = json.loads(response.text)
                        facebook_dict['publication'] = []
                        for elem in response['data']:
                            elem['created_at'] = str(datetime.datetime.strptime(elem['created_time'],
                                                                                "%Y-%m-%dT%H:%M:%S+%f").ctime())
                            del elem['created_time']
                            facebook_dict['publication'].append(elem)
                        facebook_dict['error'] = False
                    else:
                        facebook_dict['error'] = True
                except Exception as e:
                    facebook_dict['error'] = True
            else:
                return None
            return facebook_dict
        return False
    return False


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def my_social_wall(request):
    """
    Function who return all the information about the social informations
    :param request:
    :return:
    """
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except MyUser.DoesNotExist:
        return Response({
            "msg": _("MSG_USER_NOT_EXIST"),
            "status": 404
        }, status=404)
    social_wall = {'twitter': twitter_wall(user), 'instagram': instagram_wall(user), 'facebook': facebook_wall(user)}
    return Response({
        "msg": _('MSG_SOCIAL_WALL'),
        "wall": social_wall,
        "status": 200,
    }, status=200)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def company_social_wall(request, id):
    """
    Function who return all the information about the company social informations
    :param id: id of the company
    :param request:
    :return:
    """
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except MyUser.DoesNotExist:
        return Response({
            "msg": _("MSG_USER_NOT_EXIST"),
            "status": 404
        }, status=404)
    try:
        company = Company.objects.get(pk=id)
    except Company.DoesNotExist:
        return Response({
            "msg": _("MSG_COMPANY_NOT_EXIST"),
            "status": 404
        }, status=404)
    social_wall = {'twitter': twitter_wall(company.owner), 'instagram': instagram_wall(company.owner),
                   'facebook': facebook_wall(user)}
    return Response({
        "msg": _('MSG_SOCIAL_WALL'),
        "wall": social_wall,
        "status": 200,
    }, status=200)
