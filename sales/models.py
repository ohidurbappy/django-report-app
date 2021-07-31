from profiles.models import Profile
from django.db import models
from products.models import Product
from customers.models import Customer
from django.utils import timezone
from django.shortcuts import reverse
import uuid
# helper function


def generate_code():
    code = str(uuid.uuid4()).replace('-', '')[:12]
    return code


class Position(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField(blank=True)
    created = models.DateTimeField(blank=True)

    def __str__(self) -> str:
        return f"{self.id} - product: {self.product.name} quantity: {self.quantity}"

    def get_sales_id(self):
        sale_obj = self.sale_set.first()
        return sale_obj.id
    def get_customer_name(self):
        sale_obj = self.sale_set.first()
        return sale_obj.customer.name

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        return super().save(*args, **kwargs)


class Sale(models.Model):
    transaction_id = models.CharField(max_length=12, blank=12)
    positions = models.ManyToManyField(Position)
    total_price = models.FloatField(blank=True, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    salesman = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created = models.DateTimeField(blank=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"$ {self.total_price} by {self.salesman}"

    def get_absolute_url(self):
        return reverse("sales:detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        if self.transaction_id == "":
            self.transaction_id = generate_code()

        if self.created is None:
            self.created = timezone.now()

        return super().save(*args, **kwargs)

    def get_positions(self):
        return self.positions.all()


class CSV(models.Model):
    filename = models.FileField(max_length=120)
    csv_file = models.FileField(upload_to='csv',null=True)
    # activated = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.filename)
