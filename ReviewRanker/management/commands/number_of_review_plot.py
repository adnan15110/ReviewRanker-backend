from django.core.management.base import BaseCommand
from django.conf import settings
import os
from ReviewRanker.models import ProductDetails,Review
from django.conf import settings

import numpy as np
import pandas as pd
import scipy
import matplotlib.pyplot as plt

class Command(BaseCommand):
    help = 'creates the number of review frequency plot.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        products = ProductDetails.objects.all().order_by('-number_of_reviews').values_list('number_of_reviews', flat=True)[::1]
        x=np.array(products)
        mean_x=np.mean(x)
        mean_median = np.median(x)
        # # An "interface" to matplotlib.axes.Axes.hist() method
        n, bins, patches = plt.hist(x=x, bins='auto', color='#0504aa', alpha=1.0, rwidth=1.00)
        plt.grid(axis='y', alpha=1.00)
        plt.xlabel('#reviews')
        plt.ylabel('#products')
        plt.title('Frequecy of number of reviews')
        plt.text(23, 45, r'$\mu={:.2f}, median={}$'.format(mean_x, mean_median))
        maxfreq = n.max()
        plt.savefig('num_reviews_products.svg')




