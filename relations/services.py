import datetime
from uuid import UUID

from django.db.models import Q

from relations.models import UserCottageRent


def is_cottage_available(cottage_id: UUID, start_date, end_date: datetime.date) -> bool:
    """Return True if cottage is available else False"""
    existing_rents = UserCottageRent.objects.filter(cottage_id=cottage_id)
    is_available = not existing_rents.filter(
        Q(start_date__gte=start_date, start_date__lt=end_date) |
        Q(start_date__lte=start_date, end_date__gt=start_date)
    ).exists()

    return is_available
