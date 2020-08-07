"""
    Route for homepage tabs
"""

from django.utils import timezone

from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework.decorators import api_view
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from tools.json import ApiJsonResponse
from django.http import JsonResponse
from tools.serializer import serialize_promotion_object
from social_network.models.user_social_action import UserSocialAction
from ..models import Favorite


from favorite.models import Highlight
from promotion.models import Promotion


@api_view(['POST'])
def new(request):
    """
    This function permit to return all the promotion order by release date
    Args:
        request:
    Returns:
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
        promotions = Promotion.objects.filter(type_of_promotion='public').order_by('-created')
    except ObjectDoesNotExist:
        response.set_data("[]")
        response.set_result_code(200)
        response.set_result_msg("MSG_NO_PROMOTION_FOUNDED")
        return JsonResponse(response.get_dict())
    for promotion in promotions:
        favorite = False
        user_actions = None
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
            if promotion.end_date > timezone.now():
                response.set_multiples_data(serialize_promotion_object(promotion, favorite, user_actions))
        else:
            if promotion.end_date > timezone.now():
                response.set_multiples_data(serialize_promotion_object(promotion, favorite, user_actions))
    response.set_result_code(200)
    response.set_result_msg("MSG_PROMOTION_FOUNDED")
    return JsonResponse(response.get_dict())


@api_view(['POST'])
def end_soon(request):
    """
    This function permit to return all the promotion order by end date
    Args:
        request:
    Returns:
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
        promotions = Promotion.objects.filter(type_of_promotion='public').order_by('end_date')
    except ObjectDoesNotExist:
        response.set_data("[]")
        response.set_result_code(200)
        response.set_result_msg("MSG_NO_PROMOTION_FOUNDED")
        return JsonResponse(response.get_dict())
    for promotion in promotions:
        favorite = False
        user_actions = None
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
            if promotion.end_date > timezone.now():
                response.set_multiples_data(serialize_promotion_object(promotion, favorite, user_actions))
        else:
            if promotion.end_date > timezone.now():
                response.set_multiples_data(serialize_promotion_object(promotion, favorite, user_actions))
    response.set_result_code(200)
    response.set_result_msg("MSG_PROMOTION_FOUNDED")
    return JsonResponse(response.get_dict())


@api_view(['POST'])
def hot(request):
    """
    This function permit to return all the promotion order by interest for the user
    Args:
        request:
    Returns:
    """
    user = None
    response = ApiJsonResponse()
    try:
        token = request.data['token']
    except Exception as e:
        return Response({
            "msg": _('ERROR_WITH_PARAMETERS'),
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
        response.set_result_msg("MSG_FIELD_REQUIRED")
        return JsonResponse(response.get_dict())
    for promotion in promotions:
        favorite = False
        user_actions = None
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
            if promotion.end_date > timezone.now():
                response.set_multiples_data(serialize_promotion_object(promotion, favorite, user_actions))
        else:
            if promotion.end_date > timezone.now():
                response.set_multiples_data(serialize_promotion_object(promotion, favorite, user_actions))
    response.set_result_code(200)
    response.set_result_msg("MSG_PROMOTION_FOUNDED")
    return JsonResponse(response.get_dict())


@api_view(['POST'])
def highlights(request):
    """
    This function permit to return all the promotion order by priority of highlight
    Args:
        request:
    Returns:
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
        highlights = Highlight.objects.all().order_by('-priority')
    except ObjectDoesNotExist:
        response.set_data("[]")
        response.set_result_code(200)
        response.set_result_msg("MSG_NO_PROMOTION_FOUNDED")
        return JsonResponse(response.get_dict())
    for highlight in highlights:
        favorite = False
        user_actions = None
        if user:
            try:
                Favorite.objects.get(promotion=highlight.promotion, user=user)
                favorite = True
            except ObjectDoesNotExist:
                pass
            try:
                user_actions = UserSocialAction.objects.get(promotion=highlight.promotion, user=user)
            except ObjectDoesNotExist:
                pass
            if highlight.end_date > timezone.now():
                response.set_multiples_data(serialize_promotion_object(highlight.promotion, favorite, user_actions))
        else:
            if highlight.end_date > timezone.now():
                response.set_multiples_data(serialize_promotion_object(highlight.promotion, favorite, user_actions))
    response.set_result_code(200)
    response.set_result_msg("MSG_PROMOTION_FOUNDED")
    return JsonResponse(response.get_dict())