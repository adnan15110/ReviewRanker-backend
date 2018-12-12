from django.core.management.base import BaseCommand
from django.conf import settings
import json
import os
from pprint import pprint
from django.db.backends.utils import rev_typecast_decimal
from ReviewRanker.models import ProductDetails, ProductStatus,Review
from datetime import datetime
from copy import deepcopy
from django.db.models import Avg

class Command(BaseCommand):
    help = 'Populate Product details table'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        product_object_list=[]
        product_ids = Review.objects.distinct('asin').values_list('asin', flat=True)[::1]

        ProductStatus.objects.all().delete()

        for id in product_ids:
            if len(id)>0:
                reviews = Review.objects.filter(asin=id)
                product = ProductStatus()

                details = ProductDetails.objects.filter(asin=id).first()
                product.asin = id
                product.number_of_reviews = details.number_of_reviews
                product.median_reviews = 0
                overall_rating = reviews.aggregate(Avg('overall_rating'))
                product.avg_product_rating = overall_rating['overall_rating__avg']
                try:
                    product.ratio_product_rating_num_review = float(product.avg_product_rating)/float(product.number_of_reviews)
                except ZeroDivisionError:
                    product.ratio_product_rating_num_review=0

                product_object_list.append(deepcopy(product))
                product.save()

            # if len(product_object_list) % 1000 == 0:
            #     ProductStatus.objects.bulk_create(product_object_list, batch_size=1000)
            #     product_object_list=[]
            #
            # ProductStatus.objects.bulk_create(product_object_list, batch_size=1000)

        print('completed')