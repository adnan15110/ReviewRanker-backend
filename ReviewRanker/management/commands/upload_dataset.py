from django.core.management.base import BaseCommand
from django.conf import settings
import json
import os
from pprint import pprint

from django.db.backends.utils import rev_typecast_decimal

from ReviewRanker.models import Review
from datetime import datetime
from copy import deepcopy

class Command(BaseCommand):
    help = 'Populate Dataset'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='Name of your file')

    def handle(self, *args, **kwargs):
        file_name = kwargs['filename']
        path = os.path.join(settings.DATASET_DIR, file_name)
        with open(path) as f:
            lines = f.readlines()
            review_obj_list=[]
            for l in lines:
                review_obj=Review()
                review = json.loads(l)
                pprint(review)
                try:
                    review_obj.reviewer_id = review['reviewerID']
                    review_name_parts = review['reviewerName'].split('\"')
                    review_obj.reviewer_name = review_name_parts[0]
                    review_obj.asin=review['asin']
                    review_obj.review_text=review['reviewText']
                    review_obj.helpful = review['helpful'][1]
                    review_obj.overall_rating = review['overall']
                    review_obj.summary = review['summary']
                    review_obj.unix_review_time = review['unixReviewTime']

                    date = review['reviewTime'].replace(',','').split(' ')
                    review_obj.review_time = datetime(month=int(date[0]),
                                                      day=int(date[1]),
                                                      year=int(date[2]))
                except:
                    print('Date error')
                    pprint(review)

                review_obj_list.append(deepcopy(review_obj))

                if len(review_obj_list)%1000 == 0:
                    Review.objects.bulk_create(review_obj_list, batch_size=500)
                    review_obj_list=[]
                else:
                    Review.objects.bulk_create(review_obj_list, batch_size=500)
                    review_obj_list = []
        print('Upload complete')









