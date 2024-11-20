from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator

text_type = str


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return(text_type(user.is_active) + text_type(user.pk)+text_type(timestamp))
       
account_activation_token = AppTokenGenerator()    