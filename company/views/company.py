"""
    Company views
"""

import base64

from tools.json import ApiJsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from company.models.contact import Contact
from company.models.company import Company
from tools.emails import send_contact_form
from tools.serializer import serialize_dashboard_promotion_object
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from account.models import MyUser
from tools.images import store_company_logo
from company.views.company_serializer import CompanySerializer
from tools.file_request import document_in_request
from promotion.models import Promotion
from django.http import JsonResponse
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from social_network.views.social_wall import twitter_wall, instagram_wall, facebook_wall
from analytics.models.promotion_numbers import PromotionNumbers
from rest_framework_jwt.settings import api_settings


@api_view(['POST'])
def registration_contact(request):
    """
    This function send a request of registration to the admin address
    Args:
        request:
    Returns:
    """
    try:
        email = request.data['email']
        phone_number = request.data['phone_number']
        company_name = request.data['company_name']
        message = request.data['message']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        Contact.objects.create(email=email, phone_number=phone_number, company_name=company_name, message=message)
    except Exception as e:
        return Response({'status': 500, 'msg': _('MSG_ERROR_SERVER')}, status=500)
    send_contact_form(email, phone_number, company_name, message)
    return Response({'status': 200, 'msg': _('MSG_CONTACT_FORM_SAVED')}, status=200)


@api_view(['POST'])
def get_company(request, id):
    """
    This function get a company with the id
    Args:
        request:
    Returns:
    :param request:
    :param id:
    """
    try:
        company = Company.objects.get(pk=id)
        token = request.data['token']
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_COMPANY_NOT_EXIST'),
            "status": 404
        }, status=404)
    user = None
    if token:
        data = {'token': token}
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']
    company_serializer = CompanySerializer()
    social_wall = {'twitter': twitter_wall(company.owner), 'instagram': instagram_wall(company.owner),
                   'facebook': facebook_wall(company.owner)}
    data = {'company': company_serializer.serialize_company_page(company, user), 'social_wall': social_wall}
    return Response({'status': 200, 'msg': data}, status=200)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_company_information(request):
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        company = Company.objects.get(owner=user)
    except Exception:
        return Response({
            "msg": _('MSG_COMPANY_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        logo = document_in_request('logo', request.FILES)
        country = request.data['country']
        region = request.data['region']
        username = request.data['username']
        phone_number = request.data['phone_number']
        prefix_number = request.data['prefix_number']
        address = request.data['address']
        city = request.data['city']
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
    if logo:
        store_company_logo(logo, company)
    if country != "":
        company.country = country
    if region != "":
        company.region = region
    if prefix_number != "" and phone_number != "":
        tmp = user.phone_number
        user.phone_number = "+" + prefix_number + phone_number
        if tmp != user.phone_number:
            user.phone_number_verification = False
    if address != "":
        company.address = address
    if city != "":
        company.city = city
    if region != "":
        company.region = region
    user.save()
    company.save()
    if token is not None:
        return Response({
            'token': token,
            'status': 200,
            'msg': _('MSG_COMPANY_INFORMATION_RETRIEVED')
        }, status=200)
    return Response({
        'status': 200,
        'msg': _('MSG_COMPANY_INFORMATION_RETRIEVED')
    }, status=200)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def retrieve_company_informations(request):
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        company = Company.objects.get(owner=user)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_COMPANY_NOT_EXIST'),
            "status": 404
        }, status=404)
    company_serializer = CompanySerializer()
    company_data = company_serializer.serialize_company(company, user)
    return Response({
        'user_informations': company_data,
        'msg': _('MSG_COMPANY_INFORMATION_RETRIEVED')
    }, status=200)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_promotion(request, id):
    """
    API endpoint for getting a promotion object
    Args:
        request:
    Returns: promotion object

    """
    response = ApiJsonResponse()
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=id)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('NO_PROMOTION_FOUNDED'),
            "status": 404
        }, status=404)
    if promotion.company.owner == user:
        response.set_data(serialize_dashboard_promotion_object(promotion))
        response.set_result_code(200)
        response.set_result_msg("MSG_PROMOTIONS_NOT_FOUNDED")
        return JsonResponse(response.get_dict())
    return Response({
        "msg": _('MSG_USER_IS_NOT_THE_OWNER'),
        "status": 404
    }, status=404)



@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def retrieve_company_campaign(request):
    """
        This endpoint return all the campaign from a company
    :param request:
    :return:
    """
    response = ApiJsonResponse()
    try:
        user = MyUser.objects.get(pk=request.user.pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_USER_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        company = Company.objects.get(owner=user)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_COMPANY_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        campaigns = Promotion.objects.filter(company=company)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_CAMPAIGNS_NOT_EXIST'),
            "status": 404
        }, status=404)
    for campaign in campaigns:
        analytics = PromotionNumbers.objects.filter(promotion=campaign).last()
        response.set_multiples_data(serialize_dashboard_promotion_object(campaign, analytics))
    response.set_result_code(200)
    response.set_result_msg("MSG_PROMOTIONS_FOUNDED")
    return JsonResponse(response.get_dict())
