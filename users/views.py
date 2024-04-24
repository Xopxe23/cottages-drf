import datetime

from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import EmailVerification
from users.serializers import UserPasswordUpdateSerializer, UserSerializer, UserUpdateInfoSerializer
from users.services import create_email_verification
from users.tasks import send_email_verification


@swagger_auto_schema(
    method="post",
    request_body=UserSerializer,
)
@api_view(['POST'])
def register_user_view(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'success': 'Registration complete'}, status=status.HTTP_201_CREATED)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        },
        required=['email', 'password'],
    ),
)
@api_view(['POST'])
@ensure_csrf_cookie
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')
    email = email.lower()
    user = authenticate(request, email=email, password=password)
    if user:
        login(request, user)
        return Response({'success': 'Logged in'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response({'success': 'Logged out'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile_view(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    methods=["put", "patch"],
    request_body=UserUpdateInfoSerializer,
)
@api_view(['PUT', "PATCH"])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
    serializer = UserUpdateInfoSerializer(request.user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    methods=["put"],
    request_body=UserPasswordUpdateSerializer,
)
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_password_view(request):
    user = request.user
    serializer = UserPasswordUpdateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if user.check_password(serializer.validated_data.get('current_password')):
        new_password = serializer.validated_data.get('new_password')
        user.set_password(new_password)
        user.save()
        return Response({'detail': 'Password updated successfully.'}, status=status.HTTP_200_OK)
    else:
        return Response({'detail': 'Invalid current password.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def email_verification_request_view(request):
    user = request.user
    EmailVerification.objects.filter(user=user).delete()
    if request.user.is_verified:
        return Response({"error": "You're already verified"}, status=status.HTTP_200_OK)
    email_verification = create_email_verification(user)
    send_email_verification.delay(user.pk, email_verification.pk)
    return Response({"success": "Check your email"}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'code': openapi.Schema(type=openapi.TYPE_STRING)
        },
        required=['code'],
    ),
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def email_verification_view(request):
    user = request.user
    code = request.data.get("code")
    if not code:
        return Response({'error': 'Please provide code'}, status=status.HTTP_400_BAD_REQUEST)
    email_verification = EmailVerification.objects.filter(user=user, pk=code).first()
    if not email_verification:
        return Response({'error': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)
    expired = email_verification.expiration
    email_verification.delete()
    if datetime.now() > expired:
        return Response({'error': 'Code expired'}, status=status.HTTP_400_BAD_REQUEST)
    user.is_verified = True
    user.save()
    return Response({"success": "Your email is verified"}, status=status.HTTP_200_OK)
