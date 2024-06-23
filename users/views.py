from dependency_injector.wiring import Provide, inject
from django.contrib.auth import login
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.containers import Container
from users.serializers import UserSerializer, VerifyCodeSerializer
from users.services import UserServiceProtocol


@api_view(['POST'])
@inject
def register_view(
        request: Request,
        user_service: UserServiceProtocol = Provide[Container.user_service],
) -> Response:
    serializer = UserSerializer(data=request.data)
    email = serializer.initial_data.get('email')
    user_service.delete_inactive_user_by_email(email)
    user = user_service.get_active_user_by_email(email)
    if user:
        return Response({"error": "User exists"}, status=status.HTTP_400_BAD_REQUEST)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    user = serializer.save()
    user_service.send_verification_code(user)
    return Response({'success': 'Verification code sent'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@inject
def verify_register_view(
        request: Request,
        user_service: UserServiceProtocol = Provide[Container.user_service],
) -> Response:
    serializer = VerifyCodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    email = serializer.validated_data.get('email')
    code = serializer.validated_data.get('code')
    verify_code = user_service.get_code_by_email(code, email)
    if not verify_code:
        return Response({'error': 'Invalid verify code'}, status=status.HTTP_400_BAD_REQUEST)
    if not user_service.check_verification_code_not_expired(verify_code):
        return Response({'error': 'Verify code expired'}, status=status.HTTP_400_BAD_REQUEST)
    user = verify_code.user
    user.is_active = True
    user.save()
    user_service.delete_verification_codes_for_user(user)
    return Response({"status": "Your profile is verified"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@inject
def login_view(
        request: Request,
        user_service: UserServiceProtocol = Provide[Container.user_service],
) -> Response:
    email = request.data.get('email')
    user = user_service.get_active_user_by_email(email)
    if not user:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    user_service.send_verification_code(user)
    return Response({'success': 'Verification code sent'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@inject
def verify_login_view(
        request: Request,
        user_service: UserServiceProtocol = Provide[Container.user_service],
) -> Response:
    serializer = VerifyCodeSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    email = serializer.validated_data.get('email')
    code = serializer.validated_data.get('code')
    user = user_service.get_active_user_by_email(email)
    if not user:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    verify_code = user_service.get_code_by_email(code, email)
    if not verify_code:
        return Response({'error': 'Invalid verify code'}, status=status.HTTP_400_BAD_REQUEST)
    if not user_service.check_verification_code_not_expired(verify_code):
        return Response({'error': 'Verify code expired'}, status=status.HTTP_400_BAD_REQUEST)
    user_service.delete_verification_codes_for_user(user)
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
