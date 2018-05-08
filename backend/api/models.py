from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class UserProfile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  balance = models.IntegerField()

class Product(models.Model):
  name = models.CharField(max_length=200)
  price = models.IntegerField()
  image = models.ImageField(upload_to='uploaded_images/')

class Transaction(models.Model):
  user = models.ForeignKey('UserProfile', on_delete=models.SET_NULL, null=True)
  product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
  timestamp = models.DateTimeField(auto_now=True)
  price = models.IntegerField()

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)