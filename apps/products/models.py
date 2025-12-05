from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Fruits', 'Fruits'),
        ('Vegetables', 'Vegetables'),
        ('Herbal Products', 'Herbal Products'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES , default='Fruits', )
    description = models.TextField(default="No description available")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.FloatField(default=0)
    reviews = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/images/')

    def __str__(self):
        return self.name
