from uuid import UUID

from dateutil.relativedelta import relativedelta

from relations.models import UserCottageRent


def occupied_dates(cottage_id: UUID) -> dict:
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
