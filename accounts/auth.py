from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

class EmailOrUsernameBackend(ModelBackend):
    """
    Custom authentication backend that allows login using username or email.
    """

    def authenticate(self, request, username=None, password=None):
        if username is None:
            username = password = None
        else:
            try:
                user = get_user_model().objects.get(Q(username__iexact=username) | Q(email__iexact=username))
            except get_user_model().DoesNotExist:
                user = None

        if (user is not None) and (user.is_active) and self.user_can_authenticate(user):
            if user.check_password(password):
                return user
        return None