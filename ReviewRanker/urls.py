from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from ReviewRanker.views import ReviewList, ProductSearchById

urlpatterns = [
    path('reviews/', ReviewList.as_view()),
    path('product-search/', ProductSearchById.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)