import datetime
from uuid import UUID

from rest_framework_simplejwt.tokens import RefreshToken

from users.models import EmailVerification


def create_email_verification(user_id: UUID) -> EmailVerification:
    """Create email verification for current user"""
    expiration = datetime.datetime.now() + datetime.timedelta(hours=48)
    email_verification = EmailVerification.objects.create(user=user_id, expiration=expiration)
    return email_verification


def get_tokens(user_id: UUID) -> dict:
    """Returns tokens for user"""
    refresh = RefreshToken.for_user(user_id)
    access_token = str(refresh.access_token)

    return {
        'access_token': access_token,
        'refresh_token': str(refresh),
    }
