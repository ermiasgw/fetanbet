from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class CustomBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        if email is None or password is None:
            return None
        try:
            user = UserModel._default_manager.get_by_natural_key(email)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user