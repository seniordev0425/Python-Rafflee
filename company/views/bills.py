"""
    Bills views
"""

import io
import datetime
import base64

from django.core.files import File
from tools.render_pdf import render_to_pdf
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from tools.json import ApiJsonResponse
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from tools.serializer import serialize_bill_object

from account.models import MyUser
from company.models import Bills, Company


def create_bill_pdf(obj):
    """
    API endpoint for create bill
    Args:
        obj:
        request:
    Returns: HttpResponse
    """
    data = {
        'today': datetime.date.today(),
        'amount': obj.price,
        'customer_name': obj.company.company_name,
        'order_id': obj.pk,
    }
    pdf = render_to_pdf('pdf/invoice.html', data)
    filename = obj.company.company_name + '_' + obj.promotion.campaign_name + '_' + \
               datetime.datetime.now().strftime("%Y-%m-%d") + '.pdf'
    obj.bill.save(filename, File(io.BytesIO(pdf.content)))


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_bills(request):
    """
    Retrieve all the bills for a company
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
        company = Company.objects.get(owner=user)
    except ObjectDoesNotExist:
        return Response({
            "msg": _('MSG_COMPANY_NOT_EXIST'),
            "status": 404
        }, status=404)
    try:
        bills = Bills.objects.filter(company=company)
    except ObjectDoesNotExist:
        response.set_error(1)
        response.set_result_code(404)
        response.set_result_msg("MSG_NO_BILLS_FOUNDED")
        return JsonResponse(response.get_dict())
    try:
        for bill in bills:
            response.set_multiples_data(serialize_bill_object(bill))
    except Exception:
        response.set_multiples_data(serialize_bill_object(bills))
    response.set_result_code(200)
    response.set_result_msg("MSG_PROMOTION_FOUNDED")
    return JsonResponse(response.get_dict())


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_bill_with_pdf(request, id):
    """
    Retrieve a bill with the pdf
    Args:
        request:
    Returns:
    """
    response = ApiJsonResponse()
    try:
        bill = Bills.objects.get(pk=id)
    except ObjectDoesNotExist:
        response.set_error(1)
        response.set_result_code(404)
        response.set_result_msg("MSG_NO_BILLS_FOUNDED")
        return JsonResponse(response.get_dict())
    try:
        with open(bill.bill.path, "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
    except Exception:
        response.set_error(1)
        response.set_result_code(404)
        response.set_result_msg("`MSG_NO_BILL_PDF_FOUNDED`")
        return JsonResponse(response.get_dict())
    response.set_data(encoded_string.decode("utf-8"))
    response.set_result_code(200)
    response.set_result_msg("MSG_BILL_PDF_FOUNDED")
    return JsonResponse(response.get_dict())
