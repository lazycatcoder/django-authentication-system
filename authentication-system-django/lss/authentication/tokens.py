from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class TokenGenerator(PasswordResetTokenGenerator):
    # Method to create a unique hash value based on user and timestamp
    def __make_hash_value(self, user, timestamp):
        return (text_type(user.pk) + text_type(timestamp))

generate_token = TokenGenerator()