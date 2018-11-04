import ipdb
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from ReviewRanker.serializers import ReviewSerializer, ProductSearchSerializer
from ReviewRanker.models import Review
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.

class ReviewList(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ReviewSerializer
    def get_queryset(self):
        product_id = self.request.GET['asin']
        return Review.objects.filter(asin=product_id)[:10]

class ProductSearchById(ListAPIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = ProductSearchSerializer

    def get(self, request, format=None):
        queryString = self.request.GET['queryString']
        querySet = Review.objects.distinct('asin').filter(asin__icontains=queryString)[:10]
        data = ProductSearchSerializer(querySet, many=True).data
        return Response({'data': data})

    # def get_queryset(self):
    #     queryString = self.request.GET['queryString']
    #     return Review.objects.distinct('asin').filter(asin__icontains=queryString)[:10]


