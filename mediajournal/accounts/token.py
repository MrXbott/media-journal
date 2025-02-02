from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp: int) -> str:
        return f'{user.id}{timestamp}{user.is_active}'
    
email_verification_token = EmailVerificationTokenGenerator()

