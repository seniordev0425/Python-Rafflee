"""
    File who contqins all the functions about the verification of the phone number
"""

from twilio.rest import Client
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from account.models import MyUser
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def send_confirmation_number_sms(request):
    try:
        number = request.data['number']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        verify = client.verify.services(settings.TWILIO_SERVICE_SID)
        result = verify.verifications.create(to=number, channel='sms')
    except Exception as e:
        return Response({
            "msg": _('MSG_PHONE_NUMBER_ERROR'),
            "status": 404
        }, status=404)
    return Response({
        'status': 200,
        'msg': _('MSG_SMS_SENDED')
    }, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def verification_code_sms(request):
    try:
        number = request.data['number']
        code = request.data['code']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        verify = client.verify.services(settings.TWILIO_SERVICE_SID)
        result = verify.verification_checks.create(to=number, code=code)
    except Exception as e:
        return Response({
            "msg": "MSG_ERROR_CODE_NOT_CORRESPONDING",
            "status": 404
        }, status=404)
    if result.status == 'approved':
        user.phone_number_verification = True
        user.phone_number = number
        user.save()
        return Response({
            'status': 200,
            'msg': _('MSG_PHONE_NUMBER_CONFIRMED')
        }, status=200)
