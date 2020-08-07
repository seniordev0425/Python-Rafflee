"""
    List of promotions views
"""

import logging
import datetime


from django.utils import timezone
from rafflee import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from promotion.models.promotion import Promotion
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from tools.json import ApiJsonResponse
from tools.serializer import serialize_promotion_object, serialize_winning_object_for_user
from django.http import JsonResponse
from favorite.models import Favorite
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from social_network.models.user_social_action import UserSocialAction
from analytics.models.promotion_numbers import PromotionNumbers
from django.contrib.auth.hashers import PBKDF2PasswordHasher
from company.models import Company
from promotion.views.finish_promotion import close_promotion as drawing_promotion

from account.models import MyUser
from coupon.models import Coupon

logger = logging.getLogger("django")


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def campaign_id(request):
    """

    API endpoint for listing the promotion on the analytics page
    :param request: request parameters
    :returns:
    :rtype: HttpResponse
    """

    user = None
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
    except:
        return Response({
            "msg": _('MSG_COMPANY_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        promotions = Promotion.objects.filter(company=company)
    except ObjectDoesNotExist:
        response.set_data("[]")
        response.set_result_code(200)
        response.set_result_msg("MSG_PROMOTIONS_NOT_FOUNDED")
        return JsonResponse(response.get_dict())
    list_of_promotions = []
    for promotion in promotions:
        list_of_promotions.append({'name': promotion.campaign_name, 'id': promotion.pk})
    return Response({
        "msg": _('MSG_PROMOTION_FOUNDED'),
        "list_of_promotions": list_of_promotions,
        "status": 200
    }, status=200)



@api_view(['POST'])
def homepage_promotion(request):
    """

    API endpoint for listing the promotion on the dashboard page
    :param request: request parameters
    :returns:
    :rtype: HttpResponse
    """

    user = None
    response = ApiJsonResponse()
    try:
        token = request.data['token']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    if token:
        data = {'token': token}
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']
    try:
        promotions = Promotion.objects.filter(type_of_promotion='public')
    except ObjectDoesNotExist:
        response.set_data("[]")
        response.set_result_code(200)
        response.set_result_msg("MSG_PROMOTIONS_NOT_FOUNDED")
        return JsonResponse(response.get_dict())
    for promotion in promotions:
        user_actions = None
        favorite = False
        if user:
            try:
                Favorite.objects.get(promotion=promotion, user=user)
                favorite = True
            except ObjectDoesNotExist:
                pass
            try:
                user_actions = UserSocialAction.objects.get(promotion=promotion, user=user)
            except ObjectDoesNotExist:
                pass
        response.set_multiples_data(serialize_promotion_object(promotion, favorite, user_actions))
    response.set_result_code(200)
    response.set_result_msg("MSG_PROMOTIONS_FOUNDED")
    return JsonResponse(response.get_dict())


@api_view(['POST'])
def get_promotion(request, id):
    """
    API endpoint for getting a promotion object
    Args:
        request:
    Returns: promotion object

    """
    user = None
    response = ApiJsonResponse()
    try:
        token = request.data['token']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    if token:
        data = {'token': token}
        valid_data = VerifyJSONWebTokenSerializer().validate(data)
        user = valid_data['user']
    try:
        promotion = Promotion.objects.get(pk=id)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_PROMOTIONS_NOT_FOUNDED'),
            "status": 404
        }, status=404)
    user_actions = None
    favorite = False
    if user:
        try:
            Favorite.objects.get(promotion=promotion, user=user)
            favorite = True
        except ObjectDoesNotExist:
            pass
        try:
            user_actions = UserSocialAction.objects.get(promotion=promotion, user=user)
        except ObjectDoesNotExist:
            pass
    try:
        analytics = PromotionNumbers.objects.filter(promotion=promotion).last()
        analytics.click_views = analytics.click_views + 1
        analytics.save()
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_WITH_ANALYTICS'),
            "status": 404
        }, status=404)
    response.set_data(serialize_promotion_object(promotion, favorite, user_actions))
    response.set_result_code(200)
    response.set_result_msg("MSG_PROMOTIONS_FOUNDED")
    return JsonResponse(response.get_dict())


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def prizes_inventory(request):
    """

    API endpoint for getting all the user prizes object in the inventory
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
        coupons = Coupon.objects.filter(user=user)
    except ObjectDoesNotExist:
        response.set_data("[]")
        response.set_result_code(200)
        response.set_result_msg("MSG_PROMOTIONS_NOT_FOUNDED")
        return JsonResponse(response.get_dict())
    for coupon in coupons:
        if coupon.visible:
            try:
                winning_object = coupon.promotion.winnings.get(name=coupon.name)
            except Exception:
                return Response({
                    "msg": _('MSG_ERROR_WITH_SERIALIZER'),
                    "status": 500
                }, status=500)
            response.set_multiples_data(serialize_winning_object_for_user(winning_object, coupon.promotion))
    response.set_result_code(200)
    response.set_result_msg("MSG_PROMOTIONS_FOUNDED")
    return JsonResponse(response.get_dict())


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_my_promotions_in_progress(request):
    """

    API endpoint for getting all the user promotion object in progress
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
        coupons = UserSocialAction.objects.filter(user=user, distributed=False).order_by('-pk')
    except ObjectDoesNotExist:
        response.set_data("[]")
        response.set_result_code(200)
        response.set_result_msg("MSG_PROMOTIONS_NOT_FOUNDED")
        return JsonResponse(response.get_dict())
    for coupon in coupons:
        favorite = False
        user_actions = None
        try:
            Favorite.objects.get(promotion=coupon.promotion, user=user)
            favorite = True
        except ObjectDoesNotExist:
            pass
        try:
            user_actions = UserSocialAction.objects.get(promotion=coupon.promotion, user=user)
        except ObjectDoesNotExist:
            pass
        response.set_multiples_data(serialize_promotion_object(coupon.promotion, favorite, user_actions))
    response.set_result_code(200)
    response.set_result_msg("MSG_PROMOTIONS_FOUNDED")
    return JsonResponse(response.get_dict())


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def close_promotion(request):
    """
    API endpoint for closing the promotion
    Args:
        request:
    Returns: promotion object
    """
    try:
        promotion_id = request.data['promotion_id']
        password = request.data['password']
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
    hashed = PBKDF2PasswordHasher()
    try:
        password_hash = hashed.encode(password, settings.HASH_PASSWD)
    except AssertionError:
        return Response({
            "msg": _("MSG_PASSWORD_PROBLEM"),
            "status": 400
        }, status=400)
    if password_hash == user.password:
        try:
            promotion = Promotion.objects.get(pk=promotion_id)
        except ObjectDoesNotExist:
            return Response({
                "msg": _('MSG_PROMOTION_NOT_EXIST'),
                "status": 404
            }, status=404)
        if promotion.company.owner == user:
            promotion.end_date = datetime.datetime.now()
            promotion.save()
            drawing_promotion(promotion)
            return Response({
                "msg": _('MSG_PROMOTION_IS_STOPPED'),
                "status": 200,
                "promotion_id": promotion.pk,
                "end_date": promotion.end_date
            }, status=200)
        else:
            return Response({
                "msg": _('MSG_USER_IS_NOT_THE_OWNER'),
                "status": 404
            }, status=404)
    return Response({
        "msg": _('MSG_PASSWORDS_DONT_MATCH'),
        "status": 404
    }, status=404)



@api_view(['GET'])
def get_prizes_details(request, id, name):
    """
    API endpoint for closing the promotion
    Args:
        request:
    Returns: promotion object
    """
    try:
        promotion_id = id
        name = name
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        promotion = Promotion.objects.get(pk=promotion_id)
    except Exception as e:
        return Response({
            "msg": _('MSG_PROMOTION_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        prize = promotion.winnings.get(name=name)
    except Exception as e:
        return Response({
            "msg": _('MSG_NO_WINNING_OBJECT'),
            "status": 404
        }, status=404)
    return Response({"name": prize.name, "number_of_eligible_people": prize.number_of_eligible_people,
                     "image_url": prize.image_url, "description": prize.description}, status=200)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_history_promotion(request):
    """

    API endpoint for getting all the user promotion object finished
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
        coupons = Coupon.objects.filter(user=user, distributed=True)
    except ObjectDoesNotExist:
        response.set_data("[]")
        response.set_result_code(200)
        response.set_result_msg("MSG_PROMOTIONS_NOT_FOUNDED")
        return JsonResponse(response.get_dict())
    favorite = False
    user_actions = None
    for coupon in coupons:
        favorite = False
        try:
            Favorite.objects.get(promotion=coupon.promotion, user=user)
            favorite = True
        except ObjectDoesNotExist:
            pass
        try:
            user_actions = UserSocialAction.objects.get(promotion=coupon.promotion, user=user)
        except ObjectDoesNotExist:
            pass
#        if coupon.promotion.end_date < timezone.now():
        response.set_multiples_data(serialize_promotion_object(coupon.promotion, favorite, user_actions))
    response.set_result_code(200)
    response.set_result_msg("MSG_PROMOTIONS_FOUNDED")
    return JsonResponse(response.get_dict())
