import datetime
from uuid import UUID

from users.models import EmailVerification


def create_email_verification(user_id: UUID) -> EmailVerification:
    """Create email verification for current user"""
    expiration = datetime.datetime.now() + datetime.timedelta(hours=48)
    email_verification = EmailVerification.objects.create(user=user_id, expiration=expiration)
    return email_verification
