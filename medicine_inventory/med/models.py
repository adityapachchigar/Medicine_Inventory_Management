from django.db import models

# Create your models here.

class Stock(models.Model):
    doses_choice = [('Tablet','Tablet'),('Capsule','Capsule'),('Liquid','Liquid'),('Injection','Injection')]
    doses = models.CharField(max_length=10,choices=doses_choice)
    med_name = models.CharField(max_length=30)
    quantity = models.IntegerField()
    mrp = models.IntegerField()
    batch_no = models.CharField(max_length=10)
    expiry_date = models.DateField()
    amount = models.IntegerField(default=0)