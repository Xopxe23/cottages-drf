import time

from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_email_verification(user_email, verification_code):
    time.sleep(5)
    send_mail(
        "Verify your account",
        f"Your verification code: {verification_code}",
        from_email="admin@admin.com",
        recipient_list=[user_email],
        fail_silently=False,
    )
    return verification_code
