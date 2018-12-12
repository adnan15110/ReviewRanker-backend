from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Review(models.Model):
    reviewer_id = models.CharField(max_length=100, db_index=True)
    reviewer_name = models.CharField(max_length=100, db_index=True)
    asin=models.CharField(max_length=100, db_index=True)
    review_text = models.TextField(max_length=15000, null=True)
    overall_rating = models.FloatField(null=True)
    helpful = models.IntegerField(blank=True, default=0)
    summary = models.CharField(max_length=1000, null=True)
    unix_review_time = models.CharField(max_length=100, null=True)
    review_time = models.DateField(null=True)

    class Meta:
        db_table = 'reviews'

    def __str__(self):
        return "{} - {}".format(self.reviewer_name, self.helpful)

class ProductDetails(models.Model):
    product_name = models.CharField(max_length=1000, null=True)
    asin=models.CharField(max_length=100, db_index=True)
    successful=models.BooleanField(default=False)
    url=models.CharField(max_length=100)
    file_name=models.CharField(max_length=100)
    number_of_reviews = models.IntegerField(default=0)

    class Meta:
        db_table = 'product_details'

    def __str__(self):
        return "{} - {}".format(self.product_name, self.asin)

class ReviewerStatus(models.Model):
    reviewer_id = models.CharField(max_length=100, db_index=True)
    reviewer_name = models.CharField(max_length=100, db_index=True)
    review_count = models.IntegerField(default=0)
    average_helpful_score=models.FloatField(default=0)
    average_review_length=models.FloatField(default=0)
    average_review_word_count = models.FloatField(default=0)
    average_overall_rating=models.FloatField(default=0)

    median_helpful_score = models.FloatField(default=0)
    median_review_length = models.FloatField(default=0)
    median_review_word_count = models.FloatField(default=0)
    median_overall_rating = models.FloatField(default=0)

    class Meta:
        db_table = 'reviewer'

    def __str__(self):
        return "{} - {}".format(self.reviewer_name, self.reviewer_id)

class ProductStatus(models.Model):
    asin=models.CharField(max_length=100, db_index=True)
    number_of_reviews = models.IntegerField(default=0)
    mean_of_reviews = models.IntegerField(default=0)
    median_reviews  = models.IntegerField(default=0)
    avg_product_rating = models.FloatField(default=0)
    ratio_product_rating_num_review = models.FloatField(default=0)

    class Meta:
        db_table = 'product'

    def __str__(self):
        return "{} - {}".format(self.product_name, self.asin)