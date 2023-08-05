from django.contrib.auth.tokens import PasswordResetTokenGenerator

from six import text_type

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, User, timestamp):
        return(
            text_type(User.pk) + text_type(timestamp)
        )
        
generate_token = TokenGenerator()