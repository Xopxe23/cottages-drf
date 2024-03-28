from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authentication import CSRFCheck
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication


class EnforceCSRFMiddleware(MiddlewareMixin):
    def __call__(self, request):
        check = CSRFCheck(request.META.get('CSRF_COOKIE'))
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        if reason:
            raise PermissionDenied('CSRF Failed: %s' % reason)

        response = self.get_response(request)
        return response


class JWTCookieAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)

        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT['AUTH_ACCESS_COOKIE']) or None
        else:
            raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
