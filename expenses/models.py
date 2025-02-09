from django.db import models
from django.contrib.auth.models import User

class ExpenseModel(models.Model):
    CATEGORY_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]

    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)  
    date = models.DateField()
    description = models.TextField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  

    def __str__(self):
        return self.name

    