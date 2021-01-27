from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


#make an abstract class and use it in any model where you require created_at and updated_at fields
class TimeStampMixin(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractUser):
    pass

"""signal to create Portfolio instance when User is created"""
@receiver(post_save, sender=User)
def create_portfolio(sender, instance, created, **kwargs):
    if created:
        Portfolio.objects.create(user=instance)



class Stock(models.Model):
    symbol = models.CharField(max_length=6)
    name = models.CharField(max_length=120)
    exchange = models.CharField(max_length=10)

    def __str__(self):
        return f"Symbol: {self.symbol} Company Name: {self.name}"
    

class Portfolio(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="owner")


class Holding(TimeStampMixin):
    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name="stock"
    )
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="holdings"
    )


