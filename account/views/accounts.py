"""
    Accounts views
"""

from rafflee import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from tools.password import password_check
from tools.emails import reset_password_email
from tools.tokens import ACCOUNT_ACTIVATION_TOKEN
from account.models import MyUser


@api_view(['POST'])
def reset_password(request):
    """
    Password reset endpoint
    :param request: Http request with email, token, password and password_confirmation
    :return: None
    """
    try:
        user_id = request.data['id']
        token = request.data['token']
        password = request.data['password']
        password_confirmation = request.data['password_confirmation']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=user_id)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    if ACCOUNT_ACTIVATION_TOKEN.check_token(user, token):
        if password == password_confirmation:
            hash = PBKDF2PasswordHasher()
            try:
                password_hash = hash.encode(password, settings.HASH_PASSWD)
                user.password = password_hash
                user.save()
                return Response({'status': 200, 'msg': _('MSG_PASSWORD_UPDATED')}, status=200)
            except AssertionError:
                return Response({'status': 500, 'msg': _('MSG_ERROR_SERVER')}, status=500)
        return Response({'status': 404, 'msg': _('MSG_PASSWORDS_DONT_MATCH')}, status=404)
    return Response({'status': 404, 'msg': _('MSG_BAD_REQUEST')}, status=404)


@api_view(['POST'])
def send_reset_password(request):
    """
    API endpoint for sending an email for reset the password
    Args:
        request:
    Returns: HttpResponse

    """
    try:
        email = request.data['email']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(email=email)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    reset_password_email(user)
    return Response({
        "msg": _('MSG_EMAIL_RESET_PASSWORD_SENDED'),
        "status": 200
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_password(request):
    """
    API endpoint for change the user password
    Args:
        request:
    Returns: HttpResponse

    """
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        old_password = request.data['old_password']
        new_password = request.data['new_password']
        repeat_new_password = request.data['repeat_new_password']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    hashed = PBKDF2PasswordHasher()
    try:
        password_hash = hashed.encode(old_password, settings.HASH_PASSWD)
    except AssertionError:
        return Response({
            "msg": _("MSG_PASSWORD_PROBLEM"),
            "status": 400
        }, status=400)
    if password_hash == user.password:
        if new_password == repeat_new_password:
            if password_check(new_password):
                user.password = hashed.encode(new_password, settings.HASH_PASSWD)
                user.save()
                return Response({
                    "msg": _('MSG_PASSWORD_UPDATED'),
                    "status": 200
                }, status=200)
            else:
                return Response({
                    "msg": _('MSG_PASSWORD_TO_SIMPLE'),
                    "status": 404
                }, status=404)
        else:
            return Response({
                "msg": _('MSG_REPEAT_PASSWORD_DOES_NOT_MATCH'),
                "status": 404
            }, status=404)
    else:
        return Response({
            "msg": _('MSG_PASSWORDS_DONT_MATCH'),
            "status": 404
        }, status=404)
