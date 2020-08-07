"""
    Emails Tools
"""

import logging
import os

from rafflee import settings
from tools.tokens import ACCOUNT_ACTIVATION_TOKEN
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

LOGGER = logging.getLogger('django')
TEMPLATES_DIR = os.path.abspath(settings.EMAIL_TEMPLATES)


def reset_password_email(user):
    """
    Helper function that sends verification link for reset the password
    Args:
        user:
    Returns:
    """
    html_content = 'reset_password.html'
    token = ACCOUNT_ACTIVATION_TOKEN.make_token(user)
    mail = Mail(subject='Reset password', html=html_content, from_email=settings.NO_REPLY_EMAIL,
                recipient_list=[user.email],
                reply_to=[settings.NO_REPLY_EMAIL],
                data={
                    'id': user.id,
                    'token': token,
                    'user': user,
                    'url_backend': settings.BACKEND_URL,
                    'url_frontend': settings.FRONTEND_URL
                })
    try:
        mail.send()
    except Exception as e:
        LOGGER.debug(e)


def send_contact_form(email, phone_number, company_name, message):
    """
    Helper function that sends an email to the contact address
    Args:
        email: email of the company
        phone_number: contact number
        company_name: company name
        message: message
    Returns:
    """
    html_content = 'contact_form.html'
    mail = Mail(subject='Contact form', html=html_content, from_email=settings.CONTACT_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                reply_to=[settings.CONTACT_EMAIL],
                data={
                    'email': email,
                    'phone_number': phone_number,
                    'company_name': company_name,
                    'message': message
                })
    try:
        mail.send()
    except Exception as e:
        LOGGER.debug(e)


def send_confirmation_account(user):
    """
    Helper function that sends verification token to new user.
    :param user: User object
    :return: None
    """
    html_content = 'confirmation_account.html'
    token = ACCOUNT_ACTIVATION_TOKEN.make_token(user)
    mail = Mail(subject='Email verification', html=html_content, from_email=settings.NO_REPLY_EMAIL,
                recipient_list=[user.email],
                reply_to=[settings.NO_REPLY_EMAIL],
                data={
                    'id': user.id,
                    'token': token,
                    'user': user,
                    'url_backend': settings.BACKEND_URL,
                    'url_frontend': settings.FRONTEND_URL
                })
    try:
        mail.send()
    except Exception as e:
        LOGGER.debug(e)
        return False
    return True


def send_confirmation_account(user):
    """
    Helper function that sends verification token to new user.
    :param user: User object
    :return: None
    """
    html_content = 'confirmation_creation_account.html'
    mail = Mail(subject='Confirmation creation account', html=html_content, from_email=settings.NO_REPLY_EMAIL,
                recipient_list=[user.email],
                reply_to=[settings.NO_REPLY_EMAIL],
                data={
                    'id': user.id,
                    'user': user,
                    'url_backend': settings.BACKEND_URL,
                    'url_frontend': settings.FRONTEND_URL
                })
    try:
        mail.send()
    except Exception as e:
        LOGGER.debug(e)
        return False
    return True


def send_confirmation_account_google(user):
    """
    Helper function that sends verification token to new user.
    :param user: User object
    :return: None
    """
    html_content = 'confirmation_creation_account.html'
    mail = Mail(subject='Confirmation creation account', html=html_content, from_email=settings.NO_REPLY_EMAIL,
                recipient_list=[user.email],
                reply_to=[settings.NO_REPLY_EMAIL],
                data={
                    'id': user.id,
                    'user': user,
                    'url_backend': settings.BACKEND_URL,
                    'url_frontend': settings.FRONTEND_URL
                })
    try:
        mail.send()
    except Exception as e:
        LOGGER.debug(e)
        return False
    return True


class Mail:
    """
        Class for handling emails
    """

    def __init__(self, subject, html, from_email, recipient_list,
                 reply_to, data, text="", carbon_copy='', bcc='', attachments=''):
        LOGGER.debug('mail object init')
        self.subject = subject
        self.text = text
        self.html = html
        self.from_email = from_email
        self.recipient_list = recipient_list
        self.carbon_copy = carbon_copy
        self.bcc = bcc
        self.attachments = attachments
        self.reply_to = reply_to
        self.data = data

    def send(self):
        """
            Send an email

            :returns: None
        """
        email = EmailMultiAlternatives(
            subject=self.subject,
            body=self.text,
            from_email=self.from_email,
            to=self.recipient_list,
            bcc=self.bcc,
            cc=self.carbon_copy,
            attachments=self.attachments,
            reply_to=self.reply_to
        )
        html_content = self.__parse_template()
        email.attach_alternative(html_content, 'text/html')
        email.send()

    def __parse_template(self):
        if os.path.exists(os.path.join(TEMPLATES_DIR, self.html)):
            html = get_template(os.path.join(TEMPLATES_DIR, self.html))
            html_content = html.render(self.data)
            return html_content
        return self.html
