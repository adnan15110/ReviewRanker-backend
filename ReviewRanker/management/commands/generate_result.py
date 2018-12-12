from django.core.management.base import BaseCommand
from django.conf import settings
import json
import os
from pprint import pprint
from ReviewRanker.models import Review
from datetime import datetime
from copy import deepcopy
from ReviewRanker.models import ReviewerStatus, Review, ProductDetails, ProductStatus
from copy import deepcopy
from django.db.models import Avg
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np


class Command(BaseCommand):
    help = 'Populate Dataset'
    PRODUCT_COUNT = 100
    NETWORK_MEMBER_COUNT = 200

    PRODUCT_SELECTION = {
        1: 'products with most number of reviews',
        2: 'product with  median number of reviews',
        3: 'products with heighest product rating',
        4: 'products with higher product rating and review count ratio',
        5: 'products with lower product rating and review count ratio'
    }

    REVIEW_CHARACTERISTICS = {
        1: 'average amount of reviews from selected network',
        2: 'ratio of reviews from network and other',
        3: 'average helpfulness score of the reviews from the network',
        4: 'average word count of the review from the network',
        5: 'average number of positive reviews from the network',
        6: 'average number of negative reviews from the network',
        7: 'average number of neutral reviews  from the network'
    }

    NETWORK_SELECTION = {
        1: 'by on review count',
        2: 'by mean helpfulness',
        3: 'by median helpfulness',
        4: 'by mean review word count',
        5: 'by median review word count',
        6: 'by mean product rating',
        7: 'by median product rating'
    }
    SENTIMENT_GENERATOR = SentimentIntensityAnalyzer()

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='Name of your file')

    def handle(self, *args, **kwargs):
        file_name = kwargs['filename']
        # for p in range(1,6):
        #     for n in range(1,8):
        #         products = self.product_selection(p)
        #         networks = self.network_selection(n)
        #         result = self.get_review_characteristics(p, products, n, networks)
        #         with open('{}.json'.format(file_name), 'a') as f:
        #             json.dump("{} : {},".format("{}-{}".format(p,n), result),f)
        #             f.write('\n')
        #         pprint(result)
        # f.close()
        p,n = 5,1
        products = self.product_selection(p)
        networks = self.network_selection(n)
        result = self.get_review_characteristics(p, products, n, networks)
        pprint(result)



    def product_selection(self, code):
        # product selection
        if code == 1:
            products = ProductDetails.objects.all().order_by('-number_of_reviews').values_list('asin', flat=True)[::1]
            return products[0:self.PRODUCT_COUNT]
        elif code == 2:
            products = ProductDetails.objects.all().order_by('-number_of_reviews').values_list('number_of_reviews',
                                                                                               flat=True)[::1]
            products_array = np.array(products)
            median_reviews = np.median(products_array)
            products = ProductDetails.objects.filter(number_of_reviews=median_reviews).values_list('asin', flat=True)[
                       ::1]
            return products[0:self.PRODUCT_COUNT]
        elif code == 3:
            products = ProductStatus.objects.all().order_by('-avg_product_rating').values_list('asin', flat=True)[::1]
            return products[0:self.PRODUCT_COUNT]
        elif code == 4:
            products = ProductStatus.objects.all().order_by('-ratio_product_rating_num_review').values_list('asin',
                                                                                                            flat=True)[
                       ::1]
            return products[0:self.PRODUCT_COUNT]
        elif code == 5:
            products = ProductStatus.objects.all().order_by('ratio_product_rating_num_review').values_list('asin',
                                                                                                           flat=True)[
                       ::1]
            return products[0:self.PRODUCT_COUNT]
        else:
            print('select a code')

    def network_selection(self, code):
        if code == 1:
            network = ReviewerStatus.objects.all().order_by('-review_count').values_list('reviewer_id', flat=True)[::1]
            return network[:self.NETWORK_MEMBER_COUNT]
        elif code ==2:
            network = ReviewerStatus.objects.all().order_by('-average_helpful_score').values_list('reviewer_id', flat=True)[::1]
            return network[:self.NETWORK_MEMBER_COUNT]
        elif code ==3:
            network = ReviewerStatus.objects.all().order_by('-median_helpful_score').values_list('reviewer_id', flat=True)[
                      ::1]
            return network[:self.NETWORK_MEMBER_COUNT]
        elif code ==4:
            network = ReviewerStatus.objects.all().order_by('-average_review_word_count').values_list('reviewer_id', flat=True)[
                      ::1]
            return network[:self.NETWORK_MEMBER_COUNT]
        elif code ==5:
            network = ReviewerStatus.objects.all().order_by('-median_review_word_count').values_list('reviewer_id',
                                                                                                     flat=True)[
                      ::1]
            return network[:self.NETWORK_MEMBER_COUNT]
        elif code ==6:
            network = ReviewerStatus.objects.all().order_by('-average_overall_rating').values_list('reviewer_id',
                                                                                                     flat=True)[
                      ::1]
            return network[:self.NETWORK_MEMBER_COUNT]
        elif code ==7:
            network = ReviewerStatus.objects.all().order_by('-median_overall_rating').values_list('reviewer_id',
                                                                                                     flat=True)[
                      ::1]
            return network[:self.NETWORK_MEMBER_COUNT]
        else:
            print('network:  select a code')

    def get_sentiment_score(self,scores):
        if scores['neg']>scores['pos']:
            if scores['neg'] > scores['neu']:
                return 0, 1, 0
            else:
                return 0, 0, 1
        else:
            if scores['pos'] > scores['neu']:
                return 1, 0, 0
            else:
                return 0, 0, 1

    def get_review_characteristics(self, product_selection_code,products, network_selection_code, network):
        result={
            'product_selected_by': self.PRODUCT_SELECTION[product_selection_code],
            'product_count':self.PRODUCT_COUNT,
            'network_selected_by': self.NETWORK_SELECTION[network_selection_code],
            'network_member_count': self.NETWORK_MEMBER_COUNT,
            self.REVIEW_CHARACTERISTICS[1]:None,
            self.REVIEW_CHARACTERISTICS[2]: None,
            self.REVIEW_CHARACTERISTICS[3]: None,
            self.REVIEW_CHARACTERISTICS[4]: None,
            self.REVIEW_CHARACTERISTICS[5]: None,
            self.REVIEW_CHARACTERISTICS[6]: None,
            self.REVIEW_CHARACTERISTICS[7]: None,
        }

        reviews_count_from_network = []
        ratio_of_reviews_from_network_and_other = []
        avg_helpful_score=[]
        avg_review_word_count=[]
        # sentiment analysis
        positive_review_count=0
        negative_review_count=0
        neural_review_count=0

        for product in products:
            reviews_queryset = Review.objects.filter(asin=product)
            reviews_from_network = reviews_queryset.filter(reviewer_id__in=network)

            total_review_count = reviews_queryset.count()
            review_count_from_network = reviews_from_network.count()

            reviews_count_from_network.append(review_count_from_network)
            ratio_of_reviews_from_network_and_other.append(review_count_from_network/total_review_count)

            avg_helpfulness_score_from_network= reviews_from_network.aggregate(Avg('helpful'))['helpful__avg']
            if avg_helpfulness_score_from_network is None:
                avg_helpful_score.append(0.0)
            else:
                avg_helpful_score.append(avg_helpfulness_score_from_network)

            # Average word count
            word_count = []
            tokenizer = RegexpTokenizer(r'\w+')

            for review in reviews_from_network:
                if review.review_text:
                    scores = self.SENTIMENT_GENERATOR.polarity_scores(review.review_text)
                    pos,neg,neu = self.get_sentiment_score(scores)
                    positive_review_count+=pos
                    negative_review_count+=neg
                    neural_review_count+=neu

                    #import ipdb; ipdb.set_trace()
                    with open('polarity_data.csv', 'a') as f:
                        f.write('{},{},{},{},{},{}'.format(product, review.review_text.replace(',',''), scores['pos'], scores['neg'],scores['neu'],scores['compound']))
                        f.write('\n')

                    punc_removed = tokenizer.tokenize(review.review_text)
                    word_count.append(len(punc_removed))

            if len(word_count) > 0:
                avg_review_word_count.append(np.array(word_count).mean())
            else:
                avg_review_word_count.append(0)

        result[self.REVIEW_CHARACTERISTICS[1]] = np.array(reviews_count_from_network).mean()
        result[self.REVIEW_CHARACTERISTICS[2]] = np.array(ratio_of_reviews_from_network_and_other).mean()
        result[self.REVIEW_CHARACTERISTICS[3]] = np.array(avg_helpful_score).mean()
        result[self.REVIEW_CHARACTERISTICS[4]] = np.array(avg_review_word_count).mean()
        result[self.REVIEW_CHARACTERISTICS[5]] = float(positive_review_count/self.PRODUCT_COUNT)
        result[self.REVIEW_CHARACTERISTICS[6]] = float(negative_review_count/self.PRODUCT_COUNT)
        result[self.REVIEW_CHARACTERISTICS[7]] = float(neural_review_count/self.PRODUCT_COUNT)

        return result