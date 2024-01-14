from django.db import models

# Create your models here.
class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    price = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.price}"

class Restaurant(models.Model):
    id = models.IntegerField(primary_key= True)
    name = models.CharField(max_length=255)
    items = models.ManyToManyField(MenuItem)
    location = models.CharField(max_length = 255)

    def __str__(self):
        return self.name
