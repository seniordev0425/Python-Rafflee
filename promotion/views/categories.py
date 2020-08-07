"""
    List of promotions views
"""

import logging

from rest_framework.decorators import api_view
from promotion.models.categories import Category
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from tools.json import ApiJsonResponse
from tools.serializer import serialize_categorie_object
from django.http import JsonResponse

logger = logging.getLogger("django")


@api_view(['GET'])
def get_categories(request):
    """

    API endpoint for getting a promotion object
    Args:
        request:
    Returns: promotion object

    """
    response = ApiJsonResponse()
    try:
        categories = Category.objects.filter(activated=True)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_NO_CATEGORIES_FOUNDED'),
            "status": 404
        }, status=404)
    try:
        if not categories:
            return Response({
                "msg": _('MSG_NO_CATEGORIES_FOUNDED'),
                "status": 404
            }, status=404)
        for category in categories:
            response.set_multiples_data(serialize_categorie_object(category))
    except Exception:
        response.set_multiples_data(serialize_categorie_object(categories))
    response.set_result_code(200)
    response.set_result_msg("MSG_CATEGORIES_FOUNDED")
    return JsonResponse(response.get_dict())
