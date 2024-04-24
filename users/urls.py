from django.urls import include, path

from users.views import (
    email_verification_request_view,
    email_verification_view,
    login_view,
    logout_view,
    register_user_view,
    update_password_view,
    update_profile_view,
    user_profile_view,
)

urlpatterns = [
    path("register/", register_user_view, name="register"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('me/', user_profile_view, name='profile'),
    path('update-info/', update_profile_view, name='profile-update'),
    path('update-password/', update_password_view, name='password-update'),
    path('', include('social_django.urls')),
    path('request-verify/', email_verification_request_view, name="request-verify"),
    path('verify/', email_verification_view, name="verify")
]
