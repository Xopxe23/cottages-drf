from django.urls import include, path

from users.views import login_view, register_view, user_profile_view, verify_login_view, verify_register_view

urlpatterns = [
    path('', include('social_django.urls')),
    path("register/", register_view, name="register"),
    path("verify-register/", verify_register_view, name="verify-register"),
    path("login/", login_view, name="login"),
    path("verify-login/", verify_login_view, name="verify-login"),
    path("me/", user_profile_view, name="me"),
]
