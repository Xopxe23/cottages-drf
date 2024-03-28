import datetime
from uuid import UUID

import jwt
from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import EmailVerification, User


def create_email_verification(user_id: UUID) -> EmailVerification:
    """Create email verification for current user"""
    expiration = datetime.datetime.now() + datetime.timedelta(hours=48)
    email_verification = EmailVerification.objects.create(user=user_id, expiration=expiration)
    return email_verification


def get_tokens(user: User) -> dict:
    """Returns tokens for user"""
    refresh = RefreshToken.for_user(user)

    return {
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
    }


def parse_token(token: str) -> dict:
    """Parse refresh token and return user_id or error"""
    try:
        decoded_token = jwt.decode(token, settings.SIMPLE_JWT["SIGNING_KEY"],
                                   algorithms=[settings.SIMPLE_JWT["ALGORITHM"]])
        user_id = decoded_token["user_id"]
        return {"user_id": user_id}
    except jwt.ExpiredSignatureError:
        return {"error": "Token expired"}
    except jwt.InvalidTokenError:
        return {"error": "Invalid Token"}


def get_response_with_cookies(user_id: UUID) -> Response:
    """Returns Response with access and refresh tokens in cookies"""
    response = Response()
    tokens = get_tokens(user_id)
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_ACCESS_COOKIE'],
        value=tokens["access_token"],
        expires=datetime.datetime.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    )
    response.set_cookie(
        key=settings.SIMPLE_JWT['AUTH_REFRESH_COOKIE'],
        value=tokens["refresh_token"],
        expires=datetime.datetime.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    )
    return response
