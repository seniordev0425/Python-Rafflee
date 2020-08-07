"""
    Image functions
"""

import logging
import time

from rafflee import settings
from .swift_api import write_user_docs, read_last_user_docs

logger = logging.getLogger("django")


def store_profil_picture(data, user):
    """
        Method to store the profil picture of the user

        :param data: JSON to be stored
        :type data: dict
        :returns: None
    """
    timestamp = time.time()
    path = '{}/{}/{}/{}.png'.format(settings.FOLDER_DOCS,
                                    user.pk,
                                    settings.FOLDER_USER_IMAGE,
                                    int(timestamp))
    user.profile_picture_url = write_user_docs(path, data)
    user.save()


def store_winnings_image(data, winning):
    """
        Method to store the winning picture

        :param data: JSON to be stored
        :type data: dict
        :returns: None
    """
    timestamp = time.time()
    path = '{}/{}/{}/{}.png'.format(settings.FOLDER_DOCS,
                                    winning.pk,
                                    settings.FOLDER_IMG_GIVEWAY,
                                    int(timestamp))
    winning.image_url = write_user_docs(path, data)
    winning.save()


def store_company_logo(data, company):
    """
    Method to store the logo of a company
    :return:
    """
    timestamp = time.time()
    path = '{}/{}/{}/{}.png'.format(settings.FOLDER_DOCS,
                                    company.pk,
                                    settings.FOLDER_COMPANY_LOGO,
                                    int(timestamp))
    company.logo_url = write_user_docs(path, data)
    company.save()


def store_campaign_picture(data, promotion):
    """
    Method to store the logo of a campaign
    :return:
    """
    timestamp = time.time()
    path = '{}/{}/{}/{}.png'.format(settings.FOLDER_DOCS,
                                    promotion.pk,
                                    settings.FOLDER_CAMPAIGN_LOGO,
                                    int(timestamp))
    promotion.campaign_image_url = write_user_docs(path, data)
    promotion.save()


def get_company_logo(company):
    """
        Method to get the profil picture of the user

        :param company:
        :param data: JSON to be stored
        :type data: dict
        :returns: None
    """
    timestamp = time.time()
    path = '{}/{}/{}/'.format(settings.FOLDER_DOCS,
                              company.pk,
                              settings.FOLDER_COMPANY_LOGO)
    if not settings.SWIFT_USERFILES:
        return read_last_user_docs(path)
    else:
        return company.logo_url


def get_promotion_image(promotion):
    """
        Method to get the picture of the promotion

        :param promotion:
        :param data: JSON to be stored
        :type data: dict
        :returns: None
        """
    timestamp = time.time()
    path = '{}/{}/{}/'.format(settings.FOLDER_DOCS,
                              promotion.pk,
                              settings.FOLDER_CAMPAIGN_LOGO)
    if not settings.SWIFT_USERFILES:
        return read_last_user_docs(path)
    else:
        return promotion.campaign_image_url


def get_profil_picture(user):
    """
        Method to get the profil picture of the user

        :param data: JSON to be stored
        :type data: dict
        :returns: None
    """
    timestamp = time.time()
    path = '{}/{}/{}/'.format(settings.FOLDER_DOCS,
                              user.pk,
                              settings.FOLDER_USER_IMAGE)
    if not settings.SWIFT_USERFILES:
        return read_last_user_docs(path)
    else:
        return user.profile_picture_url


def get_winning_picture(winning):
    """
        Method to get the picture of the winning object

        :param data: JSON to be stored
        :type data: dict
        :returns: None
    """
    timestamp = time.time()
    path = '{}/{}/{}/'.format(settings.FOLDER_DOCS,
                              winning.pk,
                              settings.FOLDER_IMG_GIVEWAY)
    if not settings.SWIFT_USERFILES:
        return read_last_user_docs(path)
    else:
        return winning.image_url