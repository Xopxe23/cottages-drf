from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task
def send_email_verification(user_email: str, verification_code: str) -> str:
    """
    Asynchronous task to send email verification code.

    :param user_email: Email address of the user.
    :param verification_code: Verification code to be sent.
    :return: Verification code sent
    """
    send_mail(
        "Verify your account",
        f"Your verification code: {verification_code}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_email],
        fail_silently=False,
    )
    return verification_code
