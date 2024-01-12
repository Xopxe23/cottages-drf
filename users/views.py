import datetime

from django.contrib.auth import authenticate, login, logout
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import EmailVerification, User
from users.serializers import UserSerializer
from users.tasks import send_email_verification


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = serializer.instance

        return Response({
            'user_id': user.id,
            'email': user.email,
            'phone_number': user.phone_number,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_active': user.is_active,
            'is_staff': user.is_staff,
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['email', 'password'],
        ),
    )
    def post(self, request):

        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return Response({'success': 'Logged in'}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):

    def post(self, request):
        logout(request)
        return Response({'success': 'Logged out'}, status=status.HTTP_200_OK)


class UserProfileView(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            serializer = UserSerializer(user)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({'error': 'User is not authenticated'}, status.HTTP_401_UNAUTHORIZED)


class EmailVerificationRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        EmailVerification.objects.filter(user=user).delete()
        if request.user.is_verified:
            return Response({"error": "you're already verified"}, status.HTTP_200_OK)
        expiration = datetime.datetime.now() + datetime.timedelta(hours=48)
        email_verification = EmailVerification.objects.create(
            user=user,
            expiration=expiration
        )
        send_email_verification.delay(user.pk, email_verification.pk)
        return Response({"success": "Check your email"}, status.HTTP_200_OK)


class EmailVerificationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        code = request.data.get("code")
        if not code:
            return Response({'error': 'Please give code'}, status.HTTP_400_BAD_REQUEST)
        email_verification = EmailVerification.objects.filter(user=user, pk=code).first()
        if not email_verification:
            return Response({'error': 'Bad code'}, status.HTTP_400_BAD_REQUEST)
        expired = email_verification.expiration
        email_verification.delete()
        if datetime.datetime.now() > expired:
            return Response({'error': 'Code expired'}, status.HTTP_400_BAD_REQUEST)
        user.is_verified = True
        user.save()
        return Response({"success": "You're email is verified"}, status.HTTP_200_OK)
