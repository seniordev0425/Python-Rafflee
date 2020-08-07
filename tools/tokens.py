"""
    File who contqins all the functions about the generation of the tokens
"""

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


class TokenGenerator(PasswordResetTokenGenerator):
    """
        Class that generates a limited lifetime token
    """

    def _make_hash_value(self, user, timestamp):
        """
            Ensure results are consistent across DB backends

            :param user: user instance
            :param timestamp: moment of token creation
            :returns: hash value
            :rtype: string

        """
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


ACCOUNT_ACTIVATION_TOKEN = TokenGenerator()
