"""
    View for the creation of reports
"""

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from report.models import Report


@api_view(['POST'])
def creation_report_test(request):
    """

    API endpoint for reporting
    :param request: request parameters
    :returns:
    :rtype: HttpResponse
    """

    try:
        context = request.data['context']
        type = request.data['type']
        description = request.data['description']
    except Exception as e:
        return Response({
            "msg": _('MSG_FIELD_REQUIRED'),
            "status": 404
        }, status=404)
    try:
        Report.objects.create(context=context, type=type, description=description)
    except Exception:
        return Response({
            "msg": _('MSG_ERROR_WITH_REPORT'),
            "status": 404
        }, status=404)
    return Response({
        "msg": _('MSG_REPORT_SENDED'),
        "status": 200,
    }, status=200)
