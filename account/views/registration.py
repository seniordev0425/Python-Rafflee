"""
    Registration View
"""

import logging
import re
import random

from django.shortcuts import redirect
from rest_framework.permissions import IsAuthenticated

from rafflee import settings
from account.models import MyUser, Wall
from company.models import Company
from social_network.models.social_connection import SocialConnection
from social_network.models.social_network import SocialNetwork
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from tools.emails import send_confirmation_account
from tools.tokens import ACCOUNT_ACTIVATION_TOKEN
from tools.password import password_check

logger = logging.getLogger("django")


def generate_random_id():
    result = False
    while not result:
        random_number = random.randint(1000, 99999)
        try:
            Company.objects.get(id_company=random_number)
        except ObjectDoesNotExist:
            return random_number


@api_view(['GET'])
@permission_classes(())
def activate(request, pk, token):
    """
        API endpoint to activate a user after receiving an email

        :param request: request parameters
        :param pk: user primary key
        :param token: limited lifetime token
        :return:
    """
    try:
        user = MyUser.objects.get(pk=pk)
    except ObjectDoesNotExist:
        user = None
    logger.debug(
        "User activation request. user_id: %s, token: %s", pk, token)
    if user.is_active:
        logger.info(
            "User activation failed. Account is already activated. user_id: %s, token: %s", pk, token)
        return Response({
            'msg': _('MSG_ACCOUNT_ACTIVATED')
        }, status=200)
    if user is not None and ACCOUNT_ACTIVATION_TOKEN.check_token(user, token):
        user.is_active = True
        user.save()
    return Response({
        'msg': _('MSG_ERROR_WITH_THE_CONFIRMATION_ACCOUNT')
    }, status=404)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def deactivate_profile_endpoint(request):
    """
    Delete user profile route.
    :param request: Http Request
    :return: Template
    """
    try:
        password = request.data['password']
        user = MyUser.objects.get(pk=request.user.pk)
        hashed = PBKDF2PasswordHasher()
        try:
            password_hash = hashed.encode(password, settings.HASH_PASSWD)
        except AssertionError:
            return Response({
                "msg": _("MSG_PASSWORD_PROBLEM"),
                "status": 500
            }, status=500)
        if password_hash == user.password:
            user.is_active = False
            return Response({
                "msg": _('MSG_USER_DEACTIVATE'),
                "status": 200
            }, status=200)
        return Response({
            "msg": _('MSG_PASSWORDS_DONT_MATCH'),
            "status": 400
        }, status=400)
    except ObjectDoesNotExist as e:
        logger.debug(e)
        return Response({
            "msg": _("MSG_ERROR_DELETE"),
            "status": 400
        }, status=400)

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_profile_email_endpoint(request, pk, token):
    """
    Delete user profile route. Handles link that is sent in mail with token.
    :param request: Http Request
    :param email: User email
    :param token: Token sent in mail
    :return: Template
    """
    try:
        user = MyUser.objects.get(pk=pk)
        if user is not None and ACCOUNT_ACTIVATION_TOKEN.check_token(user, token):
            user.delete()
            return redirect(settings.FRONTEND_URL)
    except ObjectDoesNotExist:
        return redirect(settings.FRONTEND_URL)


@api_view(['POST'])
def register_particular(request):
    """
    API endpoint for user registration
    Args:
        request:

    Returns:

    """

    try:
        username = request.data['username']
        email = request.data['email']
        password = request.data['password1']
        confirm_password = request.data['password2']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    if password and password == confirm_password:
        if password_check(password):
            try:
                user = MyUser.objects.get(username=username)
                return Response({
                    "msg": _('MSG_USERNAME_ALREADY_EXIST'),
                    "status": 404
                }, status=404)
            except ObjectDoesNotExist:
                pass
            try:
                user = MyUser.objects.get(email=email)
                return Response({
                    "msg": _('MSG_EMAIL_ALREADY_EXIST'),
                    "status": 404
                }, status=404)
            except ObjectDoesNotExist:
                pass
            hashed = PBKDF2PasswordHasher()
            try:
                password_hash = hashed.encode(password, settings.HASH_PASSWD)
            except AssertionError:
                logger.debug("Assertion Error - Password")
                return Response({
                    "msg": _("MSG_PASSWORD_PROBLEM"),
                    "status": 400
                }, status=400)
            new_user = MyUser.objects.create(username=username, email=email, password=password_hash, is_active=False,
                                             social_connection=SocialConnection.objects.create(),
                                             settings_wall=Wall.objects.create())
            result = send_confirmation_account(new_user)
            if result:
                return Response({
                    "msg": _('MSG_USER_CREATED'),
                    "status": 200
                }, status=200)
            new_user.delete()
            return Response({
                "msg": _('MSG_ERROR_WITH_SENDING_EMAIL'),
                "status": 404
            }, status=404)
        else:
            return Response({
                "msg": _('MSG_PASSWORD_TO_SIMPLE'),
                "status": 404
            }, status=404)
    else:
        return Response({
            "msg": _('MSG_INVALID_PASSWORD'),
            "status": 404
        }, status=404)


@api_view(['POST'])
def register_professional(request):

    """
    API endpoint for company registration
        :param request: request parameters
        :returns:
        :rtype: HttpResponse
    """
    try:
        username = request.data['username']
        email = request.data['email']
        password = request.data['password1']
        confirm_password = request.data['password2']
        company_name = request.data['entity_name']
        is_company = request.data['is_company']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    if is_company == 'true':
        is_company = 'company'
    else:
        is_company = 'influencer'
    if password and password == confirm_password:
        if password_check(password):
            try:
                user = MyUser.objects.get(username=username)
                return Response({
                    "msg": _('MSG_USERNAME_ALREADY_EXIST'),
                    "status": 404
                }, status=404)
            except ObjectDoesNotExist:
                pass
            try:
                user = MyUser.objects.get(email=email)
                return Response({
                    "msg": _('MSG_EMAIL_ALREADY_EXIST'),
                    "status": 404
                }, status=404)
            except ObjectDoesNotExist:
                pass
            hashed = PBKDF2PasswordHasher()
            try:
                password_hash = hashed.encode(password, settings.HASH_PASSWD)
            except AssertionError:
                logger.debug("Assertion Error - Password")
                return Response({
                    "msg": _("MSG_PASSWORD_PROBLEM"),
                    "status": 400
                }, status=400)
            try:
                company = Company.objects.get(company_name=company_name)
                return Response({
                    "msg": _('MSG_COMPANY_NAME_ALREADY_EXIST'),
                    "status": 404
                }, status=404)
            except ObjectDoesNotExist:
                pass
            new_user = MyUser.objects.create(username=username, email=email, password=password_hash,
                                             is_active=False, company_account=True,
                                             social_connection=SocialConnection.objects.create(),
                                             settings_wall=Wall.objects.create())
            Company.objects.create(id_company=generate_random_id(), owner=new_user, company_name=company_name,
                                   type_of_account=is_company, social_network=SocialNetwork.objects.create())
            send_confirmation_account(new_user)
            return Response({
                "msg": _('MSG_USER_AND_COMPANY_CREATED'),
                "status": 200
            }, status=200)
        else:
            return Response({
                "msg": _('MSG_PASSWORD_TO_SIMPLE'),
                "status": 404
            }, status=404)
    else:
        return Response({
            "msg": _('MSG_PASSWORDS_DONT_MATCH'),
            "status": 404
        }, status=404)
