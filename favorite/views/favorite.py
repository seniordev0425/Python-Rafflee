"""
    Route for favorite's users
"""

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from tools.json import ApiJsonResponse
from django.http import JsonResponse
from tools.serializer import serialize_favorite_object, serialize_favorite_company_object

from favorite.models import Favorite, Subscription
from account.models import MyUser
from promotion.models import Promotion
from company.models import Company


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def remove_newsletter(request):
    """
    This function permit to remove newsletter subscription for an user
    Args:
        request:
    Returns:
    """
    try:
        company_pk = request.data['company_id']
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
        company = Company.objects.get(pk=company_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_NO_PROMOTION_FOUNDED'),
            "status": 404
        }, status=404)
    try:
        subscription = Subscription.objects.get(user=user, company=company)
        subscription.newsletter = False
        return Response({
            "msg": _('MSG_SUBSCRIPTION_NEWSLETTER_DELETED'),
            "company_id": company.pk,
            "status": 200
        }, status=200)
    except:
        return Response({
            "msg": _('MSG_SUBSCRIPTION_NEWSLETTER_DOES_NOT_EXIST'),
            "company_id": company.pk,
            "status": 500
        }, status=500)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def remove_follow(request):
    """
    This function permit to remove follow subscription for an user
    Args:
        request:
    Returns:
    """
    try:
        company_pk = request.data['company_id']
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
        company = Company.objects.get(pk=company_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_NO_PROMOTION_FOUNDED'),
            "status": 404
        }, status=404)
    try:
        subscription = Subscription.objects.get(user=user, company=company)
        subscription.follow = False
        return Response({
            "msg": _('MSG_SUBSCRIPTION_FOLLOW_DELETED'),
            "company_id": company.pk,
            "status": 200
        }, status=200)
    except:
        return Response({
            "msg": _('MSG_SUBSCRIPTION_FOLLOW_DOES_NOT_EXIST'),
            "company_id": company.pk,
            "status": 500
        }, status=500)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_favorite(request):
    """
    This function permit to add favorite promotion for an user
    Args:
        request:
    Returns:
    """
    try:
        promotion_pk = request.data['promotion_id']
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
        promotion = Promotion.objects.get(pk=promotion_pk)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_NO_PROMOTION_FOUNDED'),
            "status": 200
        }, status=200)
    try:
        favorite = Favorite.objects.get(user=user, promotion=promotion)
        favorite.delete()
        promotion.followers = promotion.followers - 1
        promotion.save()
        return Response({
            "msg": _('MSG_FAVORITE_DELETED'),
            "promotion_id": promotion.pk,
            "status": 200
        }, status=200)
    except ObjectDoesNotExist:
        favorite = Favorite.objects.create(user=user, promotion=promotion)
        promotion.followers = promotion.followers + 1
        promotion.save()
        return Response({
            "msg": _('MSG_FAVORITE_ADDED'),
            "promotion_id": promotion.pk,
            "status": 200
        }, status=200)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def list_favorites_campaign(request):
    """
    This function permit to return all the favorite promotion for an user
    Args:
        request:
    Returns:
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
        favorites = Favorite.objects.filter(user=user)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_FAVORITE_NOT_FOUNDED'),
            "status": 200
        }, status=200)
    try:
        if not favorites:
            return Response({
                "msg": _('MSG_NO_FAVORITE_FOUNDED'),
                "status": 200
            }, status=200)
        for favorite in favorites:
            response.set_multiples_data(serialize_favorite_object(favorite))
    except Exception:
        response.set_multiples_data(serialize_favorite_object(favorites))
    response.set_result_code(200)
    response.set_result_msg("MSG_FAVORITE_FOUNDED")
    return JsonResponse(response.get_dict())


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def list_favorites_company(request):
    """
    This function permit to return all the favorite promotion for an user
    Args:
        request:
    Returns:
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
        favorites = Subscription.objects.filter(user=user, follow=True)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_FAVORITE_COMPANY_NOT_FOUNDED'),
            "status": 200
        }, status=200)
    try:
        if not favorites:
            return Response({
                "msg": _('MSG_NO_FAVORITE_COMPANY_FOUNDED'),
                "status": 200
            }, status=200)
        for favorite in favorites:
            response.set_multiples_data(serialize_favorite_company_object(favorite))
    except Exception:
        response.set_multiples_data(serialize_favorite_company_object(favorites))
    response.set_result_code(200)
    response.set_result_msg("MSG_FAVORITE_FOUNDED")
    return JsonResponse(response.get_dict())