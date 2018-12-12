from django.core.management.base import BaseCommand
from django.conf import settings
import json
import os
from pprint import pprint
from django.db.backends.utils import rev_typecast_decimal
from django.db.models import Avg
from ReviewRanker.models import Review
from ReviewRanker.models import ReviewerStatus
from datetime import datetime
from copy import deepcopy

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import numpy as np

class Command(BaseCommand):
    help = 'generate reviewer statistics'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        reviewers = Review.objects.all().values('reviewer_id','reviewer_name').distinct('reviewer_id')
        print("Total number of reviewer: {}".format(reviewers.count()))

        for reviewer in reviewers:
            print('Working on {}-{}'.format(reviewer['reviewer_id'], reviewer['reviewer_name']))
            reviews = Review.objects.filter(reviewer_id=reviewer['reviewer_id'])
            # review count
            count=reviews.count()
            # print("review count: {}".format(reviews.count()))

            # helpful
            avg_helpful = reviews.aggregate(Avg('helpful'))['helpful__avg']
            if avg_helpful is None:
                avg_helpful=0

            # print("average helpful score count: {}".format(avg_helpful))
            helpful_score_list = Review.objects.filter(reviewer_id=reviewer['reviewer_id']).values_list('helpful', flat=True)[::1]
            helpful_score_np_array = np.array(helpful_score_list)
            if len(helpful_score_list)>0:
                median_helpful_score = np.median(helpful_score_np_array)
            else:
                median_helpful_score=0

            #averageoverall rating
            avg_overall_rating = reviews.aggregate(Avg('overall_rating'))['overall_rating__avg']
            if avg_overall_rating is None:
                avg_overall_rating=0
            # print("average overall ratings count: {}".format(avg_overall_rating))
            overall_rating_list = Review.objects.filter(reviewer_id=reviewer['reviewer_id']).values_list('overall_rating',
                                                                                                        flat=True)[::1]
            overall_rating_list = [x for x in overall_rating_list if x is not None]
            overall_rating_np_array = np.array(overall_rating_list)

            if len(overall_rating_list)>0:
                median_overall_rating = np.median(overall_rating_np_array)
            else:
                median_overall_rating=0



            # Average word count and len count
            char_count=[]
            word_count=[]
            tokenizer = RegexpTokenizer(r'\w+')

            for review in reviews:
                if review.review_text:
                    char_count.append(len(review.review_text))
                    punc_removed = tokenizer.tokenize(review.review_text)
                    # [ w for w in punc_removed if w.lower() not in stopwords.words()]
                    word_count.append(len(punc_removed))

            if len(char_count)>0:
                avg_char_count = np.average(np.array(char_count))
                avg_word_count = np.average(np.array(word_count))
                median_char_count = np.median(np.array(char_count))
                median_word_count = np.median(np.array(word_count))
            else:
                avg_char_count = 0
                avg_word_count = 0
                median_char_count = 0
                median_word_count = 0


            reviewer_obj=ReviewerStatus()
            reviewer_obj.reviewer_id =  reviewer['reviewer_id']
            reviewer_obj.reviewer_name = reviewer['reviewer_name']
            reviewer_obj.review_count = count
            reviewer_obj.average_helpful_score = avg_helpful
            reviewer_obj.average_overall_rating = avg_overall_rating
            reviewer_obj.average_review_length = avg_char_count
            reviewer_obj.average_review_word_count = avg_word_count
            reviewer_obj.median_helpful_score = median_helpful_score
            reviewer_obj.median_overall_rating = median_overall_rating
            reviewer_obj.median_review_length = median_char_count
            reviewer_obj.median_review_word_count = median_word_count


            reviewer_obj.save()

        print('status calculation done')





