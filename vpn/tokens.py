from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.contrib.auth.models import User
from .models import GenerateCertificate


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        userid = User.objects.get(username=user).id
        username = User.objects.get(username=user).username
        return (six.text_type(userid) + six.text_type(timestamp) +
                six.text_type(username))


account_activation_token = AccountActivationTokenGenerator()
