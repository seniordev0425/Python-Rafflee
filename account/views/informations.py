"""
    Informations views
"""

import base64

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from tools.file_request import document_in_request
from tools.images import store_profil_picture
from account.models import MyUser
from .user_serializer import UserSerializer
from rest_framework_jwt.settings import api_settings


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_information(request):
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    if user.company_account:
        return Response({
            "msg": _('MSG_IS_A_COMPANY_ACCOUNT'),
            "status": 404
        }, status=404)
    try:
        profile_picture = document_in_request('profile_picture', request.FILES)
        username = request.data['username']
        country = request.data['country']
        region = request.data['region']
        birth_date = request.data['birth_date']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        phone_number = request.data['phone_number']
        prefix_number = request.data['prefix_number']
        address = request.data['address']
        city = request.data['city']
        gender = request.data['gender']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    token = None
    if username != '':
        if username == user.username:
            pass
        else:
            try:
                usr_username = MyUser.objects.get(username=username)
                return Response({
                    "msg": _('MSG_USERNAME_ALREADY_EXIST'),
                    "status": 404
                }, status=404)
            except Exception:
                user.username = username
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
    if profile_picture:
        store_profil_picture(profile_picture, user)
    if country != "":
        user.country = country
    if region != "":
        user.region = region
    if birth_date != "":
        user.date_of_birth = birth_date
    if first_name != "":
        user.first_name = first_name
    if last_name != "":
        user.last_name = last_name
    if prefix_number != "" and phone_number != "":
        tmp = user.phone_number
        user.phone_number = "+" + prefix_number + phone_number
        if user.phone_number != tmp:
            user.phone_number_verification = False
    if address != "":
        user.address = address
    if city != "":
        user.city = city
    if region != "":
        user.region = region
    if gender == 'female':
        user.gender = 'female'
    else:
        user.gender = 'male'
    user.save()
    if token is not None:
        return Response({
            'token': token,
            'status': 200,
            'msg': _('MSG_USER_INFORMATION_UPLOADED')
        }, status=200)
    return Response({
        'status': 200,
        'msg': _('MSG_USER_INFORMATION_UPLOADED')
    }, status=200)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def retrieve_informations(request):
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    if user.company_account:
        return Response({
            "msg": _('MSG_IS_A_COMPANY_ACCOUNT'),
            "status": 404
        }, status=404)
    user_serializer = UserSerializer()
    user_data = user_serializer.serialize_users(user)
    return Response({
        'user_informations': user_data,
        'msg': _('MSG_USER_INFORMATION_RETRIEVED')
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def check_username_exist(request):
    try:
        username = request.data['username']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        if username == request.user.username:
            return Response({
                "exist": False,
                "msg": _('MSG_USERNAME_NOT_EXIST'),
                "status": 200
            }, status=200)
        user = MyUser.objects.get(username=username)
        return Response({
            "exist": True,
            "msg": _('MSG_USERNAME_EXIST'),
            "status": 200
        }, status=200)
    except ObjectDoesNotExist:
        return Response({
            "exist": False,
            "msg": _('MSG_USERNAME_NOT_EXIST'),
            "status": 200
        }, status=200)
