from django.core.management.base import BaseCommand
from django.conf import settings
import json
import os
from pprint import pprint
from django.db.backends.utils import rev_typecast_decimal
from ReviewRanker.models import ProductDetails,Review
from datetime import datetime
from copy import deepcopy

class Command(BaseCommand):
    help = 'Populate Product details table'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        product_detail_object_list=[]
        review_set = Review.objects.distinct('asin')
        for review in review_set.iterator():
            product = ProductDetails()
            product.asin=review.asin
            product.product_name=review.summary
            product.successful=False
            product.url='https://www.amazon.com/dp/{}'.format(review.asin)
            product.file_name=''
            product_detail_object_list.append(deepcopy(product))

            if len(product_detail_object_list)%1000==0:
                ProductDetails.objects.bulk_create(product_detail_object_list, batch_size=1000)
                product_detail_object_list=[]

        ProductDetails.objects.bulk_create(product_detail_object_list, batch_size=1000)
        print('completed')