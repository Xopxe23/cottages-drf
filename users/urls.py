from django.urls import include, path

from users.views import (
    EmailVerificationRequestView,
    EmailVerificationView,
    LoginView,
    LogoutView,
    RegisterUserView,
    UserProfileView,
)

urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name='login'),
    path('', include('social_django.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', UserProfileView.as_view(), name='profile'),
    path('request-verify/', EmailVerificationRequestView.as_view(), name="request-verify"),
    path('verify/', EmailVerificationView.as_view(), name="verify"),
]
