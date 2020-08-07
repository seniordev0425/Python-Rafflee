"""
    File with the different JWT functions
"""

import uuid

from datetime import datetime
from calendar import timegm

from rest_framework_jwt.settings import api_settings


def jwt_get_secret_key(user_model):
    """
    Get jwt secret key
    :param user_model: User model instance
    :return: JWT Secret
    :rtype: String
    """
    return user_model.jwt_secret


def jwt_otp_payload_handler(user, device=None):
    """

    :param user:
    :return:

    Args:
        device: if user using device or not
    """
    payload = {
        'user_id': user.pk,
        'username': user.username,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }
    if isinstance(user.pk, uuid.UUID):
        payload['user_id'] = str(user.pk)
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = timegm(
            datetime.utcnow().utctimetuple()
        )
    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE
    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    if (user is not None) and (device is not None) and (device.user_id == user.id) and (device.confirmed is True):
        payload['otp_device_id'] = device.persistent_id
    else:
        payload['otp_device_id'] = None
    return payload


def jwt_response_payload_handler(token):
    """
        Handler for the payload of jwt response

        :param token: limited lifetime token
        :returns: Token and response
        :rtype: dict
    """
    return {
        'token': token,
    }