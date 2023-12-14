from django.db import models
from shops.models import Shop  # Adjust the import based on your project structure

class Item(models.Model):
    shop = models.ForeignKey(Shop, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='items/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Add other fields as necessary

    def __str__(self):
        return self.name
