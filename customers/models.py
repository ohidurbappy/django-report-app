from django.db import models

# Create your models here.


class Customer(models.Model):
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to='cusotmers', default='no_picture.png')

    def __str__(self) -> str:
        return self.name
