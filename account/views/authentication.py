"""
    Authentication views
"""

import logging
import facebook
import requests
import json
import datetime

from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from requests_oauthlib import OAuth1Session
from django.utils import timezone
from rafflee import settings
from account.models import MyUser, Connection
from company.models import Company
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from rest_framework_jwt.settings import api_settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from django.contrib.auth.models import update_last_login
from django.contrib.gis.geoip2 import GeoIP2
from tools.emails import send_confirmation_account
from social_network.models.social_connection import SocialConnection
from requests_oauthlib import OAuth2Session

logger = logging.getLogger("django")


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def logout(request):
    """

    API endpoint for user logout

        :param request: request parameters
        :returns:
        :rtype: HttpResponse
    """
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    user.last_logout = timezone.now()
    user.save(update_fields=['last_logout'])
    return Response({
        "msg": _('MSG_USER_LOGOUT'),
        "status": 200
    },status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def url_connect_facebook(request):
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except MyUser.DoesNotExist:
        return Response({
            "msg": _("MSG_USER_NOT_EXIST"),
            "status": 404
        }, status=404)
    try:
        token = request.data['token']
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        url = "https://graph.facebook.com/oauth/access_token"
        params = {
            "client_id": settings.FACEBOOK_ID,
            "client_secret": settings.FACEBOOK_SECRET,
            "fb_exchange_token": token,
            "grant_type": "fb_exchange_token"
        }
        user.social_connection.facebook_short_access_token = token
        response = requests.get(url, params=params)
        result = json.loads(response.text)
        user.social_connection.facebook_rights_connected = True
        user.social_connection.facebook_long_access_token = result['access_token']
        if 'expires_in' in result:
            user.social_connection.facebook_date_token = datetime.date.today() + \
                                                         datetime.timedelta(seconds=result['expires_in'])
        user.social_connection.save()
        try:
            graph = facebook.GraphAPI(user.social_connection.facebook_long_access_token)
            fields = ['email, name, last_name, first_name, birthday, gender']
            profile = graph.get_object('me', fields=fields)
            if user.social_connection.facebook_id != profile['id']:
                user.social_connection.facebook_id = profile['id']
                user.social_connection.save()
        except Exception as e:
            return Response({
                "msg": _("MSG_ERROR_FACEBOOK_CONNECT"),
                "status": 404
            }, status=404)
    except Exception as e:
        return Response(
            {"msg": _('MSG_ERROR_FACEBOOK_CONNECT'),
             "status": 500
             }, status=500)
    return Response({
        "msg": _('MSG_FACEBOOK_AUTHORIZATION_VALIDATED'),
        "status": 200,
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def url_connect_instagram_business(request):
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except MyUser.DoesNotExist:
        return Response({
            "msg": _("MSG_USER_NOT_EXIST"),
            "status": 404
        }, status=404)
    try:
        token = request.data['token']
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        url = "https://graph.facebook.com/oauth/access_token"
        params = {
            "client_id": settings.FACEBOOK_ID,
            "client_secret": settings.FACEBOOK_SECRET,
            "fb_exchange_token": token,
            "grant_type": "fb_exchange_token"
        }
        user.social_connection.instagram_business_short_access_token = token
        response = requests.get(url, params=params)
        result = json.loads(response.text)
        user.social_connection.instagram_business_long_access_token = result['access_token']
        if 'expires_in' in result:
            user.social_connection.instagram_business_date_token = datetime.date.today() + \
                                                         datetime.timedelta(seconds=result['expires_in'])
        user.social_connection.save()
        try:
            url = 'https://graph.facebook.com/v7.0/me/accounts'
            params = {"access_token": user.social_connection.instagram_business_long_access_token}
            response = requests.get(url, params=params)
            if response.status_code == 200:
                ret = []
                response = json.loads(response.text)
                for elem in response['data']:
                    ret.append({'name': elem['name'], 'id': elem['id']})
                return Response({
                    "msg": _('MSG_INSTAGRAM_BUSINESS_PAGE_RETURNED'),
                    "business_pages": ret,
                    "status": 200,
                }, status=200)
        except Exception as e:
            return Response({
                "msg": _("MSG_ERROR_INSTAGRAM_BUSINESS_CONNECT"),
                "status": 404
            }, status=404)
    except Exception as e:
        return Response(
            {"msg": _('MSG_ERROR_INSTAGRAM_BUSINESS_CONNECT'),
             "status": 500
             }, status=500)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def url_connect_instagram_business_validation(request):
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except Exception:
        return Response({
            "msg": _("MSG_USER_NOT_EXIST"),
            "status": 404
        }, status=404)
    try:
        id = request.data['id']
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        try:
            url = 'https://graph.facebook.com/v7.0/' + id
            params = {
                "access_token": user.social_connection.facebook_page_access_token,
#                "access_token": user.social_connection.instagram_business_long_access_token,
                "fields": "instagram_business_account{username}",
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                response = json.loads(response.text)
                user.social_connection.instagram_connected = False
                user.social_connection.instagram_business_connected = True
                user.social_connection.instagram_business_id = response['instagram_business_account']['id']
                user.social_connection.instagram_username = response['instagram_business_account']['username']
                user.social_connection.save()
                return Response({
                    "msg": _('MSG_INSTAGRAM_BUSINESS_AUTHORIZATION_VALIDATED'),
                    "status": 200,
                }, status=200)
        except Exception as e:
            return Response({
                "msg": _("MSG_ERROR_INSTAGRAM_BUSINESS_CONNECT"),
                "status": 404
            }, status=404)
    except Exception as e:
        return Response(
            {"msg": _('MSG_ERROR_INSTAGRAM_BUSINESS_CONNECT'),
             "status": 500
             }, status=500)



@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def url_connect_instagram(request):
    """
    API endpoint for the instagram access token
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
        token = request.data['token']
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    url = 'https://api.instagram.com/oauth/access_token'
    params = {
        "client_id": settings.INSTAGRAM_ID,
        "client_secret": settings.INSTAGRAM_SECRET,
        "grant_type": 'authorization_code',
        "redirect_uri": 'https://rafflee.io/instagram/connect/',
        "code": token,
    }
    response = requests.post(url, data=params)
    if response.status_code == 200:
        result = json.loads(response.text)
        try:
            user.social_connection.instagram_id = result['user_id']
            user.social_connection.instagram_short_access_token = result['access_token']
            user.social_connection.instagram_business_connected = False
            user.social_connection.save()
        except Exception:
            return Response({
                "msg": _('MSG_ERROR_INSTAGRAM_CONNECT'),
                "status": 500
            }, status=500)
        try:
            url = "https://graph.instagram.com/access_token"
            params = {
                "grant_type": "ig_exchange_token",
                "client_secret": settings.INSTAGRAM_SECRET,
                "access_token": user.social_connection.instagram_short_access_token
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                result = json.loads(response.text)
                user.social_connection.instagram_long_access_token = result['access_token']
                user.social_connection.instagram_connected = True
                user.social_connection.instagram_date_token = datetime.date.today() + \
                                                              datetime.timedelta(seconds=result['expires_in'])
                url = "https://graph.instagram.com/" + str(user.social_connection.instagram_id)
                params = {
                    "access_token": user.social_connection.instagram_long_access_token,
                    "fields": "username"
                }
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    user.social_connection.instagram_username = json.loads(response.text)['username']
                user.social_connection.save()
                return Response({
                    "msg": _('MSG_INSTAGRAM_LOGIN_VALIDATED'),
                    "status": 200,
                }, status=200)
            else:
                return Response(
                    {"msg": _('MSG_ERROR_INSTAGRAM_CONNECT'),
                     "status": 500
                     }, status=500)
        except Exception as e:
            return Response({
                "msg": _('MSG_ERROR_INSTAGRAM_CONNECT'),
                "status": 500
            }, status=500)
    else:
        return Response({
            "msg": _('MSG_ERROR_INSTAGRAM_CONNECT'),
            "status": 500
        }, status=500)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def url_connect_snapchat(request, step):
    """
    API endpoint for the snapchat access token
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
    scope = ['snapchat-marketing-api']
    redirect_url = 'https://rafflee.io/snapchat/connect/'
    authorize_url = 'https://accounts.snapchat.com/login/oauth2/authorize'
    access_token_url = 'https://accounts.snapchat.com/login/oauth2/access_token'
    profil_url = 'https://adsapi.snapchat.com/v1/me'
    if step == 1:
        try:
            oauth = OAuth2Session(settings.SNAPCHAT_ID,
                                  redirect_uri=redirect_url,
                                  scope=scope)
            authorization_url, state = oauth.authorization_url(authorize_url)
            return Response({
                "msg": _('MSG_OAUTH_SNAPCHAT_URL'),
                "status": 200,
                "url": authorization_url
            }, status=200)
        except Exception as e:
            return Response({
                "msg": _('MSG_ERROR_WITH_SNAPCHAT_URL'),
                "status": 404
            }, status=404)
    elif step == 2:
        try:
            url = request.data['url']
        except ObjectDoesNotExist:
            return Response({
                "msg": _('MSG_FIELD_REQUIRED'),
                "status": 404
            }, status=404)
        try:
            oauth = OAuth2Session(settings.SNAPCHAT_ID,
                                  redirect_uri=redirect_url,
                                  scope=scope)
            token = oauth.fetch_token(access_token_url,
                                      authorization_response=url,
                                      client_secret=settings.SNAPCHAT_SECRET,
                                      scope=scope)
            user.social_connection.snapchat_token = token['access_token']
            user.social_connection.snapchat_refresh_token = token['refresh_token']
            user.social_connection.snapchat_connected = True
            headers = {'Authorization' : 'Bearer ' + token['access_token']}
            r = requests.get(profil_url, headers=headers)
            if r.status_code == 200:
                result = json.loads(r.text)
                user.social_connection.snapchat_id = result['me']['id']
            else:
                user.social_connection.save()
                return Response({
                    "msg": _('MSG_ERROR_SNAPCHAT_USER_PROFILE'),
                    "status": 404,
                }, status=404)
            user.social_connection.save()
            return Response({
                "msg": _('MSG_SNAPCHAT_LOGIN_VALIDATED'),
                "status": 200,
            }, status=200)
        except Exception as e:
            return Response({
                "msg": _('MSG_ERROR_WITH_SNAPCHAT_OAUTH_TOKEN'),
                "error": e,
                "status": 404
            }, status=404)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def url_connect_twitch(request, version):
    """
    API endpoint for the twitch access token
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
        token = request.data['token']
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    redirect_url = None
    twitch_id = None
    twitch_secret = None
    if version == 'web':
        twitch_id = settings.TWITCH_ID
        twitch_secret = settings.TWITCH_SECRET_KEY
        redirect_url = "https://rafflee.io/twitch/connect/"
        mobile_connection = False
    elif version == 'mobile':
        twitch_id = settings.TWITCH_ID_MOBILE
        twitch_secret = settings.TWITCH_MOBILE_SECRET_KEY
        redirect_url = "rafflee://twitch/connect/"
        mobile_connection = True
    if not redirect_url:
        return Response({
            "msg": _("MSG_ERROR_WITH_URL"),
            "status": 404
        }, status=404)
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        "client_id": twitch_id,
        "client_secret": twitch_secret,
        "code": token,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_url
    }
    response = requests.post(url, params=params)
    if response.status_code == 200:
        result = json.loads(response.text)
        url = 'https://id.twitch.tv/oauth2/validate'
        headers = {'Authorization': 'OAuth ' + result['access_token']}
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            user.social_connection.twitch_token = result['access_token']
            user.social_connection.twitch_refresh_token = result['refresh_token']
            user.social_connection.twitch_id_token = result['id_token']
            user.social_connection.twitch_connected = True
            result = json.loads(r.text)
            user.social_connection.twitch_user_id = result['user_id']
            user.social_connection.twitch_client_id = result['client_id']
            user.social_connection.twitch_connected_mobile = mobile_connection
            user.social_connection.save()
            if user.company_account:
                url = 'https://api.twitch.tv/kraken/channel'
                headers = {'Accept': 'application/vnd.twitchtv.v5+json', 'Client-ID': settings.TWITCH_ID,
                           'Authorization': 'OAuth ' + user.social_connection.twitch_token}
                r = requests.get(url, headers=headers)
                result = json.loads(r.text)
                try:
                    company = Company.objects.get(owner=user)
                    print(result['_id'])
                    company.social_network.twitch_channel_id = result['_id']
                    company.social_network.twitch_channel_url = result['url']
                    company.save()
                except:
                    return Response({
                        "msg": _("COMPANY_DOES_NOT_EXIST"),
                        "status": 404
                    }, status=404)
        else:
            return Response({
                "msg": _('MSG_ERROR_WITH_TWITCH_GET_USER_INFORMATIONS'),
                "status": response.status_code
            }, status=response.status_code)
        return Response({
            "msg": _('MSG_TWITCH_LOGIN_VALIDATED'),
            "status": 200,
        }, status=200)
    else:
        return Response({
            "msg": _('MSG_ERROR_WITH_TWITCH_OAUTH_TOKEN'),
            "status": response.status_code
        }, status=response.status_code)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def url_connect_twitter(request, step):
    """
    API endpoint for the twitter access token
    :param step:
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
    if step == 1:
        try:
            request_token = OAuth1Session(client_key=settings.TWITTER_API_KEY,
                                          client_secret=settings.TWITTER_API_SECRET_KEY)
            url = 'https://api.twitter.com/oauth/request_token'
            data = request_token.get(url)
            data_token = str.split(data.text, '&')
            user.social_connection.twitter_connection_oauth_token = str.split(data_token[0], '=')[1]
            user.social_connection.twitter_connection_oauth_token_secret = str.split(data_token[1], '=')[1]
            user.social_connection.save()
            return Response({
                "msg": _('MSG_OAUTH_TOKEN_TWITTER'),
                "status": 200,
                "oauth_token": user.social_connection.twitter_connection_oauth_token
            }, status=200)
        except Exception as e:
            return Response({
                "msg": _('MSG_ERROR_WITH_TWITTER_LOGIN'),
                "status": 404
            }, status=404)
    elif step == 2:
        try:
            oauth_token = request.data['oauth_token']
            oauth_verifier = request.data['oauth_verifier']
        except ObjectDoesNotExist:
            return Response({
                "msg": _('MSG_FIELD_REQUIRED'),
                "status": 404
            }, status=404)
        try:
            if user.social_connection.twitter_connection_oauth_token == oauth_token:
                oauth_token = OAuth1Session(client_key=settings.TWITTER_API_KEY,
                                            client_secret=settings.TWITTER_API_SECRET_KEY,
                                            resource_owner_key=user.social_connection.twitter_connection_oauth_token,
                                            resource_owner_secret=user.social_connection.twitter_connection_oauth_token_secret)
                url = 'https://api.twitter.com/oauth/access_token'
                data = {"oauth_verifier": oauth_verifier}
                access_token_data = oauth_token.post(url, data=data)
                access_token_list = str.split(access_token_data.text, '&')
                user.social_connection.twitter_id = str.split(access_token_list[2], '=')[1]
                user.social_connection.twitter_oauth_token_data = str.split(access_token_list[0], '=')[1]
                user.social_connection.twitter_oauth_token_secret = str.split(access_token_list[1], '=')[1]
                user.social_connection.twitter_connected = True
                user.social_connection.save()
                return Response({
                    "msg": _('MSG_TWITTER_LOGIN_VALIDATED'),
                    "status": 200,
                }, status=200)
            else:
                return Response({
                    "msg": _('MSG_ERROR_WITH_TWITTER_OAUTH_TOKEN'),
                    "status": 404
                }, status=404)
        except Exception as e:
            return Response({
                "msg": _('MSG_ERROR_WITH_TWITTER_OAUTH_TOKEN'),
                "error": e,
                "status": 404
            }, status=404)
    elif step == 3:
        try:
            twitter_id = request.data['twitter_id']
            oauth_token = request.data['oauth_token']
            oauth_token_secret = request.data['oauth_token_secret']
        except ObjectDoesNotExist:
            return Response({
                "msg": _('MSG_FIELD_REQUIRED'),
                "status": 404
            }, status=404)
        try:
            user.social_connection.twitter_id = twitter_id
            user.social_connection.twitter_oauth_token_data = oauth_token
            user.social_connection.twitter_oauth_token_secret = oauth_token_secret
            user.social_connection.twitter_connected = True
            user.social_connection.save()
            return Response({
                "msg": _('MSG_TWITTER_LOGIN_VALIDATED'),
                "status": 200,
            }, status=200)
        except Exception as e:
            return Response({
                "msg": _('MSG_ERROR_WITH_TWITTER_OAUTH_TOKEN'),
                "error": e,
                "status": 404
            }, status=404)

@api_view(['POST'])
def login_google(request):
    """

    API endpoint for google authorization url

        :param request: request parameters
        :returns:
        :rtype: HttpResponse
    """
    try:
        code = request.data['code']
        ip = request.data['ip']
        device = request.data['device']
        device_id = request.data['device_id']
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        if device == 'web' or device == 'android':
            id_info = id_token.verify_oauth2_token(code, google_requests.Request(), settings.GOOGLE_ID_WEB)
        else:
            id_info = id_token.verify_oauth2_token(code, google_requests.Request(), settings.GOOGLE_ID_IOS)
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return Response({
                "msg": _("MSG_ERROR_LOGIN_GOOGLE_CONNECT"),
                "status": 404
            }, status=404)
    except Exception as e:
        return Response({
            "msg": _("MSG_ERROR_LOGIN_GOOGLE_CONNECT"),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(email=id_info['email'])
        if user.social_connection.google_id != id_info['sub']:
            user.social_connection.google_id = id_info['sub']
            user.save()
    except Exception:
        user = MyUser.objects.create(username=id_info['email'], email=id_info['email'], is_active=True,
                                     first_name=id_info['given_name'], last_name=id_info['family_name'],
                                     profile_picture_url=id_info['picture'],
                                     social_connection=SocialConnection.objects.create(google_id=id_info['sub']))
        result = send_confirmation_account(user)
        if not result:
            user.delete()
            return Response({
                "msg": _('MSG_ERROR_WITH_SENDING_EMAIL'),
                "status": 404
            }, status=404)
    g = GeoIP2()
    result = g.city(ip)
    connection = Connection.objects.create(ip=ip, device_id=device_id, country_name=result['country_name'],
                                           city_name=result['city'], continent_name=result['continent_name'],
                                           postal_code=result['postal_code'], region=result['region'],
                                           latitude=result['latitude'], longitude=result['longitude'], user=user)
    if user.is_active:
            if user.company_account:
                company = True
            else:
                company = False
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            update_last_login(None, user)
            connection.save()
            return Response({
                'token': token,
                'company': company,
            }, status=200)
    return Response({
        "msg": _("MSG_USER_NOT_ACTIVE"),
        "status": 400
    }, status=400)


@api_view(['POST'])
def login_facebook(request):
    """

    API endpoint for user facebook login

        :param request: request parameters
        :returns:
        :rtype: HttpResponse
    """
    try:
        access_token = request.data['access_token']
        ip = request.data['ip']
        device_id = request.data['device_id']
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        graph = facebook.GraphAPI(access_token)
        fields = ['email, name, last_name, first_name, birthday, gender']
        profile = graph.get_object('me', fields=fields)
    except Exception as e:
        return Response({
            "msg": _("MSG_ERROR_LOGIN_CONNECT"),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(email=profile['email'])
        if user.social_connection.facebook_id != profile['id']:
            user.social_connection.facebook_id = profile['id']
        user.social_connection.facebook_short_access_token = access_token
        user.social_connection.facebook_login_connected = True
        user.social_connection.save()
        user.save()
    except Exception:
        user = MyUser.objects.create(username=profile['email'], email=profile['email'], is_active=True,
                                     first_name=profile['first_name'], last_name=profile['last_name'],
                                     social_connection=SocialConnection.objects.create(facebook_id=profile['id']))
        result = send_confirmation_account(user)
        if not result:
            user.delete()
            return Response({
                "msg": _('MSG_ERROR_WITH_SENDING_EMAIL'),
                "status": 404
            }, status=404)
    g = GeoIP2()
    result = g.city(ip)
    connection = Connection.objects.create(ip=ip, device_id=device_id, country_name=result['country_name'],
                                           city_name=result['city'], continent_name=result['continent_name'],
                                           postal_code=result['postal_code'], region=result['region'],
                                           latitude=result['latitude'], longitude=result['longitude'], user=user)
    if user.is_active:
            if user.company_account:
                company = True
            else:
                company = False
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            update_last_login(None, user)
            connection.save()
            return Response({
                'token': token,
                'company': company,
            }, status=200)
    return Response({
        "msg": _("MSG_USER_NOT_ACTIVE"),
        "status": 400
    }, status=400)


@api_view(['POST'])
def mobile_login(request):
    """

    API endpoint for user login

        :param request: request parameters
        :returns:
        :rtype: HttpResponse
    """
    try:
        password = request.data['password']
        username = request.data['username']
        ip = request.data['ip']
        device_id = request.data['device_id']
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(email=username)
    except MyUser.DoesNotExist:
        try:
            user = MyUser.objects.get(username=username)
        except MyUser.DoesNotExist:
            return Response({
                "msg": _("MSG_USER_NOT_EXIST"),
                "status": 404
            }, status=404)
    g = GeoIP2()
    result = g.city(ip)
    connection = Connection.objects.create(ip=ip, device_id=device_id, country_name=result['country_name'],
                                           city_name=result['city'], continent_name=result['continent_name'],
                                           postal_code=result['postal_code'], region=result['region'])
    if user.is_active:
        hashed = PBKDF2PasswordHasher()
        try:
            password_hash = hashed.encode(password, settings.HASH_PASSWD)
        except AssertionError:
            logger.debug("Assertion Error - Password")
            return Response({
                "msg": _("MSG_PASSWORD_PROBLEM"),
                "status": 400
            }, status=400)
        if password_hash == user.password:
            connection.user = user
            if user.company_account:
                company = True
            else:
                company = False
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            update_last_login(None, user)
            connection.save()
            return Response({
                'token': token,
                'company': company,
            }, status=200)
        return Response({
            "msg": _("MSG_INVALID_PASSWORD"),
            "status": 400
        }, status=400)
    return Response({
        "msg": _("MSG_USER_NOT_ACTIVE"),
        "status": 400
    }, status=400)


@api_view(['POST'])
def login(request):
    """

    API endpoint for user login

        :param request: request parameters
        :returns:
        :rtype: HttpResponse
    """
    try:
        password = request.data['password']
        username = request.data['username']
        ip = request.data['ip']
        device_id = request.data['device_id']
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(email=username)
    except MyUser.DoesNotExist:
        try:
            user = MyUser.objects.get(username=username)
        except MyUser.DoesNotExist:
            return Response({
                "msg": _("MSG_USER_NOT_EXIST"),
                "status": 404
            }, status=404)
    g = GeoIP2()
    result = g.city(ip)
    connection = Connection.objects.create(ip=ip, device_id=device_id, country_name=result['country_name'],
                                           city_name=result['city'], continent_name=result['continent_name'],
                                           postal_code=result['postal_code'], region=result['region'],
                                           latitude=result['latitude'], longitude=result['longitude'])
    if user.is_active:
        hashed = PBKDF2PasswordHasher()
        try:
            password_hash = hashed.encode(password, settings.HASH_PASSWD)
        except AssertionError:
            logger.debug("Assertion Error - Password")
            return Response({
                "msg": _("MSG_PASSWORD_PROBLEM"),
                "status": 400
            }, status=400)
        if password_hash == user.password:
            connection.user = user
            if user.company_account:
                company = True
            else:
                company = False
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            update_last_login(None, user)
            connection.save()
            return Response({
                'token': token,
                'company': company,
            }, status=200)
        return Response({
            "msg": _("MSG_INVALID_PASSWORD"),
            "status": 400
        }, status=400)
    return Response({
        "msg": _("MSG_USER_NOT_ACTIVE"),
        "status": 400
    }, status=400)


@api_view(['POST'])
def login_professional(request):
    """

    API endpoint for user login

        :param request: request parameters
        :returns:
        :rtype: HttpResponse
    """
    try:
        password = request.data['password']
        username = request.data['username']
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        id_company, username = username.split("/")
    except Exception:
        return Response({
            "msg": _("MSG_ID_NOT_EXIST"),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(username=username)
    except MyUser.DoesNotExist:
        return Response({
            "msg": _("MSG_USER_NOT_EXIST"),
            "status": 404
        }, status=404)
    try:
        company = Company.objects.get(id_company=id_company)
    except ObjectDoesNotExist:
        return Response({
            "msg": _("COMPANY_ID_NOT_EXIST"),
            "status": 404
        }, status=404)
    if user.is_active and user.company_account and \
            (company.owner == user or user.username in company.get_contributors().split(',')):
        hashed = PBKDF2PasswordHasher()
        try:
            password_hash = hashed.encode(password, settings.HASH_PASSWD)
        except AssertionError:
            logger.debug("Assertion Error - Password")
            return Response({
                "msg": _("MSG_PASSWORD_PROBLEM"),
                "status": 400
            }, status=400)
        if password_hash == user.password:
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)
            return Response({
                'token': token,
                'company_name': company.company_name
            }, status=200)
        return Response({
            "msg": _("MSG_INVALID_PASSWORD"),
            "status": 400
        }, status=400)
    return Response({
        "msg": _("MSG_USER_NOT_ACTIVE"),
        "status": 400
    }, status=400)
