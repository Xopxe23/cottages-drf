import datetime
from uuid import UUID

from django.db.models import Q

from relations.models import UserCottageLike, UserCottageRent


def is_cottage_available(cottage_id: UUID, start_date, end_date: datetime.date) -> bool:
    """Return True if cottage is available else False"""
    existing_rents = UserCottageRent.objects.filter(cottage_id=cottage_id).exclude(status=3)
    is_available = not existing_rents.filter(
        Q(start_date__gte=start_date, start_date__lt=end_date) |
        Q(start_date__lte=start_date, end_date__gt=start_date)
    ).exists()

    return is_available


def get_liked_cottages_ids(user) -> list[UUID]:
    """Return a list of IDs of cottages liked by the user"""
    liked_cottages_list = UserCottageLike.objects.filter(user=user).values_list('cottage_id', flat=True)
    return list(liked_cottages_list)


def change_rent_status(rent_id: UUID, status: int) -> None:
    """Change rent status by id"""
    UserCottageRent.objects.filter(id=rent_id).update(status=status)
