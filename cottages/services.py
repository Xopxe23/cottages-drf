from uuid import UUID

from dateutil.relativedelta import relativedelta
from django.db.models import Avg, Prefetch, Q, QuerySet
from django.db.models.functions import Round

from cottages.models import Cottage
from relations.models import UserCottageRent, UserCottageReview


def get_cottages_list(**filter_by) -> QuerySet[Cottage]:
    """Return cottages with annotated rating"""
    cottages = Cottage.objects.filter(**filter_by).select_related("category", "town").prefetch_related(
        "images", Prefetch("reviews", queryset=UserCottageReview.objects.only("cottage", "rating"))
    ).annotate(average_rating=Round(Avg("reviews__rating"), 1))
    return cottages


def get_booked_cottages_ids(start_date, end_date: str) -> QuerySet[Cottage]:
    """Return id's of booked cottages on current dates"""
    booked_cottages = UserCottageRent.objects.filter(
        Q(start_date__gte=start_date, start_date__lt=end_date) |
        Q(start_date__lte=start_date, end_date__gt=start_date)
    ).exclude(status=3).values_list('cottage')
    return booked_cottages


def get_occupied_dates(cottage_id: UUID) -> dict:
    """Return occupied days of cottage"""
    all_dates = UserCottageRent.objects.filter(cottage=cottage_id).values_list('start_date', 'end_date')
    closed_days = []
    start_days = []
    for start_date, end_date in all_dates:
        start_days.append(start_date)
        current_date = start_date + relativedelta(days=1)
        while current_date < end_date:
            closed_days.append(current_date)
            current_date += relativedelta(days=1)
    return {"closed_days": closed_days, "start_days": start_days}


def round_ratings(data: dict) -> dict:
    """Make decimal ratings to float"""
    data['average_rating'] = round(float(data['average_rating']), 1)
    data['average_location_rating'] = round(float(data['average_location_rating']), 1)
    data['average_cleanliness_rating'] = round(float(data['average_cleanliness_rating']), 1)
    data['average_communication_rating'] = round(float(data['average_communication_rating']), 1)
    data['average_value_rating'] = round(float(data['average_value_rating']), 1)
    return data


def update_image_order(image, new_order: int, max_order: int):
    """ Update the order of an image. """
    if new_order > max_order:
        image.bottom()
    else:
        image.to(new_order)
