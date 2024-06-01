import datetime

from django.contrib.auth import login
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from users.models import User, VerifyCode
from users.serializers import UserSerializer, VerifyCodeSerializer
from users.services import delete_users_verify_codes
from users.tasks import send_email_verification


@api_view(['POST'])
def register_view(request: Request) -> Response:
    serializer = UserSerializer(data=request.data)
    email = serializer.initial_data.get('email')
    user = User.objects.filter(email=email).first()
    if user:
        if user.is_active:
            return Response({"error": "User exists"}, status=status.HTTP_400_BAD_REQUEST)
        user.delete()
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    verify_code = VerifyCode.objects.create(
        action="R",
        user=user,
    )
    send_email_verification.delay(user.email, verify_code.code)
    return Response({'success': 'Verification code sent'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def verify_register_view(request: Request) -> Response:
    serializer = VerifyCodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    email = serializer.validated_data.get('email')
    code = serializer.validated_data.get('code')
    verify_code = VerifyCode.objects.filter(user__email=email, code=code, action="R").first()
    if not verify_code:
        return Response({'error': 'Invalid verify code'}, status=status.HTTP_400_BAD_REQUEST)
    if verify_code.expires_at < datetime.datetime.now(datetime.timezone.utc):
        verify_code.delete()
        return Response({'error': 'Verify code expired'}, status=status.HTTP_400_BAD_REQUEST)
    user = verify_code.user
    user.is_active = True
    user.save()
    delete_users_verify_codes(user)
    return Response({"status": "Your profile is verified"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def login_view(request: Request) -> Response:
    email = request.data.get('email')
    user = User.objects.filter(email=email, is_active=True).first()
    if not user:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    verify_code = VerifyCode.objects.create(action='L', user=user)
    send_email_verification.delay(email, verify_code.code)
    return Response({'success': 'Verification code sent'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_login_view(request: Request) -> Response:
    serializer = VerifyCodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    email = serializer.validated_data.get('email')
    code = serializer.validated_data.get('code')
    user = User.objects.filter(email=email, is_active=True).first()
    if not user:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    verify_code = VerifyCode.objects.filter(user=user, code=code, action="L").first()
    if not verify_code:
        return Response({'error': 'Invalid verify code'}, status=status.HTTP_400_BAD_REQUEST)
    if verify_code.expires_at < datetime.datetime.now(datetime.timezone.utc):
        verify_code.delete()
        return Response({'error': 'Verify code expired'}, status=status.HTTP_400_BAD_REQUEST)
    delete_users_verify_codes(user)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return Response({'success': 'User logged in'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request: Request) -> Response:
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_info(request: Request) -> Response:
    pass
