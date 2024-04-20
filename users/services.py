import datetime

from users.models import EmailVerification, User


def create_email_verification(user: User) -> EmailVerification:
    """Create email verification for current user"""
    expiration = datetime.datetime.now() + datetime.timedelta(hours=48)
    email_verification = EmailVerification.objects.create(user=user, expiration=expiration)
    return email_verification
