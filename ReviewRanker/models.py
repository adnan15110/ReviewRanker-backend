from django.db import models

# Create your models here.

class Review(models.Model):
    reviewer_id = models.CharField(max_length=100, db_index=True)
    reviewer_name = models.CharField(max_length=100, db_index=True)
    asin=models.CharField(max_length=100, db_index=True)
    review_text = models.TextField(max_length=15000, null=True)
    overall_rating = models.FloatField(null=True)
    summary = models.CharField(max_length=1000, null=True)
    unix_review_time = models.CharField(max_length=100, null=True)
    review_time = models.DateField(null=True)

    class Meta:
        db_table = 'reviews'

    def __str__(self):
        return "{} - {}".format(self.reviewer_name, self.overall_rating)

class ProductDetails(models.Model):
    product_name = models.CharField(max_length=1000, null=True)
    asin=models.CharField(max_length=100, db_index=True)
    successful=models.BooleanField(default=False)
    url=models.CharField(max_length=100)
    file_name=models.CharField(max_length=100)

    class Meta:
        db_table = 'product_details'

    def __str__(self):
        return "{} - {}".format(self.product_name, self.asin)