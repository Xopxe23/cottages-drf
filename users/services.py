from users.models import User, VerifyCode


def delete_users_verify_codes(user: User) -> None:
    """
    Deletes all verification codes associated with the given user.

    :param user: User object for whom verification codes need to be deleted.
    :return: None
    """
    VerifyCode.objects.filter(user=user).delete()
