from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.backends import ModelBackend


class UsernameOrEmailAuthBackend(ModelBackend):
    """
    Custom authentication backend.

    Allows personals to log in using their email address or username.
    """

    def authenticate(self, request, username_email=None, password=None):
        """
        Overrides the authenticate method to allow personals to log in using their email address or username.
        """
        try:
            print(username_email)
            user = User.objects.get(
                Q(username=username_email) | Q(email=username_email))
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        """
        Overrides the get_user method to allow personals to log in using their email address or username.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
