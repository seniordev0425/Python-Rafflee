"""
    Analytics views
"""

import logging
import datetime

from datetime import timedelta
from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist
from account.models import MyUser, Connection
from company.models import Company
from analytics.models import SocialNumbers, PromotionNumbers
from tools.json import ApiJsonResponse
from django.http import JsonResponse
from promotion.models import Promotion
from social_network.models.user_social_action import UserSocialAction
from tools.serializer import serialize_analytics_social_numbers, serialize_analytics_click

logger = logging.getLogger("django")


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def followers(request, time):
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
        analytics = None
        response = ApiJsonResponse()
        if time == 'day':
            analytics = SocialNumbers.objects.filter(company=company).latest('emission_date')
            response.set_multiples_data(serialize_analytics_social_numbers(analytics))
            response.set_result_code(200)
            response.set_result_msg("MSG_OVERVIEW_ANALYTICS_FOUNDED")
            return JsonResponse(response.get_dict())
        elif time == 'week':
            analytics = SocialNumbers.objects.filter(company=company,
                                                     emission_date__range=(timezone.now().date() - timedelta(days=6),
                                                                           timezone.now().date() + timedelta(days=1))) \
                .order_by('emission_date')
        elif time == 'month':
            analytics = SocialNumbers.objects.filter(company=company,
                                                     emission_date__range=(timezone.now().date() - timedelta(days=31),
                                                                           timezone.now().date() + timedelta(days=1))) \
                .order_by('emission_date')
        elif time == 'year':
            today = datetime.date.today()
            nrb_month = 12
            analytics = []
            while nrb_month >= 0:
                if today.month - nrb_month < 1:
                    tmp_month = 12 - (nrb_month - today.month)
                    tmp_year = today.year - 1
                else:
                    tmp_month = today.month - nrb_month
                    tmp_year = today.year
                try:
                    analytic = SocialNumbers.objects.get(company=company, emission_date__month=tmp_month,
                                                         emission_date__day=1, emission_date__year=tmp_year)
                    analytics.append(analytic)
                except ObjectDoesNotExist:
                    try:
                        analytic = SocialNumbers.objects.filter(company=company, emission_date__month=tmp_month,
                                                                emission_date__year=tmp_year).last()
                        if analytic:
                            analytics.append(analytic)
                    except ObjectDoesNotExist:
                        logger.debug("Error with month")
                nrb_month = nrb_month - 1
        for analytic in analytics:
            response.set_multiples_data(serialize_analytics_social_numbers(analytic))
        response.set_result_code(200)
        response.set_result_msg("MSG_OVERVIEW_ANALYTICS_FOUNDED")
        return JsonResponse(response.get_dict())
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_NO_OVERVIEW_ANALYTICS'),
            "status": 404
        }, status=404)


def obj_all_participants(participant, all_participants):
    connection = Connection.objects.filter(user=participant).last()
    if all_participants:
        tmp = False
        for obj in all_participants:
            if obj['city'] == connection.city_name and obj['country'] == connection.country_name \
                    and obj['latitude'] == connection.latitude \
                    and obj['longitude'] == connection.longitude:
                obj['number'] = obj['number'] + 1
                tmp = True
                break
        if not tmp:
            all_participants.append({"city": connection.city_name,
                                     "continent": connection.continent_name,
                                     "latitude": connection.latitude,
                                     "longitude": connection.longitude,
                                     "number": 1, "country": connection.country_name})
    else:
        all_participants.append({"city": connection.city_name,
                                 "continent": connection.continent_name,
                                 "latitude": connection.latitude, "longitude": connection.longitude,
                                 "number": 1, "country": connection.country_name})
    return all_participants


def return_connection_participate(all_participants, promotion):
    for participant in promotion.participants.all():
        try:
            all_participants = obj_all_participants(participant, all_participants)
        except ObjectDoesNotExist:
            return 400, None
    return 200, all_participants


def return_connection_action(all_participants, promotion):
    list_of_user_action = UserSocialAction.objects.filter(promotion=promotion)
    for user_action in list_of_user_action:
        try:
            all_participants = obj_all_participants(user_action.user, all_participants)
        except ObjectDoesNotExist:
            return 400, None
    return 200, all_participants


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def map(request, id, type):
    """
    This endpoint return analytics for the map
    :param request:
    :param id:
    :param type:
    :return:
    """
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
    all_participants = []
    if id != "all":
        id = int(id)
        try:
            promotion = Promotion.objects.get(pk=id, company=company)
            if type == "action":
                status, all_participants = return_connection_action(all_participants, promotion)
            elif type == "participation":
                status, all_participants = return_connection_participate(all_participants, promotion)
        except ObjectDoesNotExist:
            return Response({
                "msg": _('MSG_PROMOTION_NOT_EXIST'),
                "status": 404
            }, status=404)
    else:
        if type == "action":
            try:
                all_promotion = Promotion.objects.filter(company=company)
            except ObjectDoesNotExist:
                return Response({
                    "msg": _('MSG_PROMOTION_NOT_EXIST'),
                    "status": 404
                }, status=404)
            for promotion in all_promotion:
                status, all_participants = return_connection_action(all_participants, promotion)
        elif type == "participation":
            promotions = Promotion.objects.filter(company=company)
            for promotion in promotions:
                status, all_participants = return_connection_participate(all_participants, promotion)
    return Response({"datas": all_participants}, status=200)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def gender(request, id):
    male = 0
    female = 0
    unknow = 0
    male_percentage = 0
    female_percentage = 0
    unknow_percentage = 0
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
    if id != "all":
        id = int(id)
        try:
            promotion = Promotion.objects.get(pk=id, company=company)
            for participant in promotion.participants.all():
                if participant.gender == 'male':
                    male = male + 1
                elif participant.gender == 'female':
                    female = female + 1
                else:
                    unknow = unknow + 1
        except ObjectDoesNotExist:
            return Response({
                "msg": _('MSG_PROMOTION_NOT_EXIST'),
                "status": 404
            }, status=404)
    else:
        try:
            promotions = Promotion.objects.filter(company=company)
            for promotion in promotions:
                if promotion.participants:
                    for participant in promotion.participants.all():
                        if participant.gender == 'male':
                            male = male + 1
                        elif participant.gender == 'female':
                            female = female + 1
                        else:
                            unknow = unknow + 1
        except ObjectDoesNotExist:
            return Response({
                "msg": _('MSG_PROMOTION_NOT_EXIST'),
                "status": 404
            }, status=404)
    if male + unknow + female > 0:
        male_percentage = ((male / (male + unknow + female)) * 100)
        female_percentage = ((female / (male + unknow + female)) * 100)
        unknow_percentage = ((unknow / (male + unknow + female)) * 100)
    return Response({
        "male": male,
        "female": female,
        "unknow": unknow,
        "male_percentage": male_percentage,
        "female_percentage": female_percentage,
        "unknow_percentage": unknow_percentage,
    }, status=200)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def clicks(request, time, id):
    """
    This function return analytics from the clicks and action participation to campaigns
    :param request:
    :param time:
    :param id:
    :return:
    """
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
        promotion = Promotion.objects.get(company=company, pk=id)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTION_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        analytics = None
        response = ApiJsonResponse()
        if time == 'day':
            analytics = PromotionNumbers.objects.filter(promotion=promotion).latest('start_date')
            response.set_multiples_data(serialize_analytics_click(analytics))
            response.set_result_code(200)
            response.set_result_msg("MSG_OVERVIEW_ANALYTICS_FOUNDED")
            return JsonResponse(response.get_dict())
        elif time == 'week':
            analytics = PromotionNumbers.objects.filter(promotion=promotion,
                                                        start_date__range=(timezone.now().date() - timedelta(days=7),
                                                                           timezone.now().date() + timedelta(days=1))) \
                .order_by('start_date')
        elif time == 'month':
            analytics = PromotionNumbers.objects.filter(promotion=promotion,
                                                        start_date__range=(timezone.now().date() - timedelta(days=31),
                                                                           timezone.now().date() + timedelta(days=1))) \
                .order_by('start_date')
        elif time == 'year':
            today = datetime.date.today()
            nrb_month = 12
            analytics = []
            while nrb_month >= 0:
                if today.month - nrb_month < 1:
                    tmp_month = 12 - (nrb_month - today.month)
                    tmp_year = today.year - 1
                else:
                    tmp_month = today.month - nrb_month
                    tmp_year = today.year
                try:
                    analytic = PromotionNumbers.objects.get(promotion=promotion,start_date__month=tmp_month,
                                                            start_date__day=1, start_date__year=tmp_year)
                    analytics.append(analytic)
                except ObjectDoesNotExist:
                    try:
                        analytic = PromotionNumbers.objects.filter(promotion=promotion, start_date__month=tmp_month,
                                                                   start_date__year=tmp_year).last()
                        if analytic:
                            analytics.append(analytic)
                    except ObjectDoesNotExist:
                        logger.debug("Error with month")
                nrb_month = nrb_month - 1
        for analytic in analytics:
            response.set_multiples_data(serialize_analytics_click(analytic))
        response.set_result_code(200)
        response.set_result_msg("MSG_OVERVIEW_ANALYTICS_FOUNDED")
        return JsonResponse(response.get_dict())
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_NO_OVERVIEW_ANALYTICS'),
            "status": 404
        }, status=404)


from datetime import date

def check_age(participant, range):
    """
    This function fill the participants on the object range
    :param range:
    :return:
    """
    today = date.today()
    age = today.year - participant.date_of_birth.year - ((today.month, today.day) <
                                                          (participant.date_of_birth.month,
                                                           participant.date_of_birth.day))
    if age >= 13 and age <= 17:
        range['13_17'] = range['13_17'] + 1
    elif age >= 18 and age <= 24:
        range['18_24'] = range['18_24'] + 1
    elif age >= 25 and age <= 34:
        range['25_34'] = range['25_34'] + 1
    elif age >= 35 and age <= 44:
        range['35_44'] = range['35_44'] + 1
    elif age >= 45 and age <= 54:
        range['45_54'] = range['45_54'] + 1
    elif age >= 55 and age <= 64:
        range['55_65'] = range['55_65'] + 1
    elif age >= 65:
        range['65'] = range['65'] + 1
    return range


def define_age_percentage(range_percentage):
    """
    This function permit to define the percentage of people
    :param range_percentage:
    :param range:
    :return:
    """
    cp = {'13_17':0, '18_24':0, '25_34':0, '35_44':0, '45_54':0, '55_65':0, '65':0}
    total = range_percentage['13_17'] + range_percentage['18_24'] + range_percentage['25_34'] + \
            range_percentage['35_44'] + range_percentage['45_54'] + range_percentage['55_65'] + \
            range_percentage['65']
    if total != 0:
        cp['13_17'] = (range_percentage['13_17']/total) * 100
        cp['18_24'] = (range_percentage['18_24']/total) * 100
        cp['25_34'] = (range_percentage['25_34']/total) * 100
        cp['35_44'] = (range_percentage['35_44']/total) * 100
        cp['45_54'] = (range_percentage['45_54']/total) * 100
        cp['55_65'] = (range_percentage['55_65']/total) * 100
        cp['65'] = (range_percentage['65']/total) * 100
    else:
        cp = range_percentage
    return cp


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def range_age(request, id, type):
    """
    This endpoint return analytics for the range of the age of the participants
    :param type:
    :param request:
    :param time:
    :param id:
    :return:
    """
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
    range_dict = {'13_17':0, '18_24':0, '25_34':0, '35_44':0, '45_54':0, '55_65':0, '65':0}
    if id == 'all':
        try:
            promotions = Promotion.objects.filter(company=company)
        except ObjectDoesNotExist:
            return Response({
                "msg": _('MSG_PROMOTION_NOT_EXIST'),
                "status": 404
            }, status=404)
        try:
            for promotion in promotions:
                for participant in promotion.participants.all():
                    if participant.date_of_birth:
                        if type == "female" and participant.gender == 'female':
                            range_dict = check_age(participant, range_dict)
                        elif type == "male" and participant.gender == 'male':
                            range_dict = check_age(participant, range_dict)
                        elif type == "all" and (participant.gender == 'male' or participant.gender == 'female'):
                            range_dict = check_age(participant, range_dict)
            return Response({"range":range_dict, "range_percentage":define_age_percentage(range_dict)}, status=200)
        except Exception as e:
            return Response({
                "e": e.args[0],
                "msg": _('MSG_NO_OVERVIEW_ANALYTICS'),
                "status": 404
            }, status=404)
    else:
        try:
            promotion = Promotion.objects.get(company=company, pk=int(id))
        except ObjectDoesNotExist:
            return Response({
                "msg": _('MSG_PROMOTION_NOT_EXIST'),
                "status": 404
            }, status=404)
        try:
            for participant in promotion.participants.all():
                if participant.date_of_birth:
                    if type == "female" and participant.gender == 'female':
                        range_dict = check_age(participant, range_dict)
                    elif type == "male" and participant.gender == 'male':
                        range_dict = check_age(participant, range_dict)
                    elif type == "all" and (participant.gender == 'male' or participant.gender == 'female'):
                        range_dict = check_age(participant, range_dict)
            return Response({"range": range_dict, "range_percentage": define_age_percentage(range_dict)}, status=200)
        except Exception as e:
            return Response({
                "e": e.args[0],
                "msg": _('MSG_NO_OVERVIEW_ANALYTICS'),
                "status": 404
            }, status=404)