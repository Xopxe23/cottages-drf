import datetime
from typing import Protocol

from users.models import User, VerifyCode
from users.tasks import send_email_verification


class CodeServiceProtocol(Protocol):

    def send_verification_code(self, user: User) -> None:
        ...

    def check_verify_code_by_email(self, code: str, email: str) -> VerifyCode | None:
        ...

    @staticmethod
    def check_verification_code_not_expired(code: VerifyCode) -> bool:
        ...

    def delete_verification_codes_for_user(self, user: User) -> None:
        ...


class UserServiceProtocol(Protocol):

    def get_active_user_by_email(self, email: str) -> User | None:
        ...

    def delete_inactive_user_by_email(self, email: str) -> None:
        ...

    def send_verification_code(self, user: User) -> None:
        ...

    def get_code_by_email(self, code: str, email: str) -> VerifyCode | None:
        ...

    def check_verification_code_not_expired(self, code: VerifyCode) -> bool:
        ...

    def delete_verification_codes_for_user(self, user: User) -> None:
        ...


class CodeService:
    model = VerifyCode.objects

    def send_verification_code(self, user: User) -> None:
        code = self._generate_verify_code(user)
        send_email_verification.delay(user.email, code.code)

    def check_verify_code_by_email(self, code: str, email: str) -> VerifyCode | None:
        return self.model.filter(user__email=email, code=code).first()

    @staticmethod
    def check_verification_code_not_expired(code: VerifyCode) -> bool:
        if code.expires_at < datetime.datetime.now(datetime.timezone.utc):
            code.delete()
            return False
        return True

    def _generate_verify_code(self, user: User) -> VerifyCode:
        return self.model.create_verify_code(user)

    def delete_verification_codes_for_user(self, user: User) -> None:
        self.model.delete_verification_codes_for_user(user)


class UserService:
    model = User.objects

    def __init__(self, code_service: CodeServiceProtocol):
        self.code_service = code_service

    def get_active_user_by_email(self, email: str) -> User | None:
        user = self._get_user_by_email(email)
        return user if user and user.is_active else None

    def delete_inactive_user_by_email(self, email: str) -> None:
        user = self._get_user_by_email(email)
        user.delete() if user else None

    def _get_user_by_email(self, email: str) -> User | None:
        return self.model.filter(email=email).first()

    def send_verification_code(self, user: User) -> None:
        self.code_service.send_verification_code(user)

    def get_code_by_email(self, code: str, email: str) -> VerifyCode | None:
        return self.code_service.check_verify_code_by_email(code, email)

    def check_verification_code_not_expired(self, code: VerifyCode) -> bool:
        return self.code_service.check_verification_code_not_expired(code)

    def delete_verification_codes_for_user(self, user: User) -> None:
        self.code_service.delete_verification_codes_for_user(user)
