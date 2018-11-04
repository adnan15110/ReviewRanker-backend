from ReviewRanker.models import Review
from rest_framework.serializers import ModelSerializer

class ReviewSerializer(ModelSerializer):
    class Meta:
        model=Review
        fields='__all__'


class ProductSearchSerializer(ModelSerializer):
    class Meta:
        model=Review
        fields=('id','asin')