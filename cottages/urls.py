from django.urls import path

from cottages.views import CottageDetail, CottageList, update_cottage_image_order
from relations.views import (
    UserCottageReviewDetail,
    UserCottageReviewList,
    add_or_remove_favorites,
    create_cottage_rent_view,
    get_current_user_cottages_view,
    get_current_user_favorites,
    get_current_user_rents_view,
)

urlpatterns = [
    path('', CottageList.as_view(), name='cottage-list'),
    path('<uuid:cottage_id>/', CottageDetail.as_view(), name='cottage-detail'),
    path('<uuid:cottage_id>/reviews/', UserCottageReviewList.as_view(), name='review-list'),
    path('<uuid:cottage_id>/reviews/<uuid:review_id>/', UserCottageReviewDetail.as_view(), name='review-detail'),
    path('<uuid:cottage_id>/create_rent/', create_cottage_rent_view, name='rents-create'),
    path('<uuid:cottage_id>/favorites/', add_or_remove_favorites, name='favorites'),
    path('my_favorites/', get_current_user_favorites, name='my-favorites'),
    path('my_rents/', get_current_user_rents_view, name='my-rents'),
    path('my_cottages/', get_current_user_cottages_view, name='my-cottages'),
    path('images/change_order/', update_cottage_image_order, name='images-update')
]
