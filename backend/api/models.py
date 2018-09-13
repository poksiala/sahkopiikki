"""
Sähköpiikki database models.
"""
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class UserProfile(models.Model):
  """User Profile model."""
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  visible = models.BooleanField(default=True)

  def balance(self):
    """Calculate user balance."""
    return "{:.2f}€".format(-sum(map(
        lambda t: t.price, self.transactions.filter(done=False))) / 100)

  def __str__(self):
    if not self.user.first_name:
      return "{} {}".format(self.user.first_name, self.user.last_name)

    return self.user.username

class Product(models.Model):
  """Product model."""
  name = models.CharField(max_length=200)
  price = models.IntegerField()
  price.help_text = 'In cents'
  image = models.ImageField(upload_to='uploaded_images/')
  visible = models.BooleanField(default=True)
  last_bought = models.DateTimeField(null=True, default=None)

  def price_in_euros(self):
    """Calculate price in euros."""
    return "{:.2f}€".format(self.price / 100)

  def __str__(self):
    return self.name

class Transaction(models.Model):
  """Transaction model."""
  user = models.ForeignKey('UserProfile', related_name='transactions',
                           on_delete=models.SET_NULL, null=True)
  product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
  timestamp = models.DateTimeField(auto_now=True)
  price = models.IntegerField()
  price.help_text = 'In cents'
  done = models.BooleanField(default=False)

  def name(self):
    """Get human readable name for transaction."""
    return str(self)

  def price_in_euros(self):
    """Calculate price in euros."""
    return "{:.2f}€".format(self.price / 100)

  def __str__(self):
    return "{:.2f}€ to {}".format(self.price / 100, self.user)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
  #pylint: disable=unused-argument
  """Create a token when a new user is created."""
  if created:
    Token.objects.create(user=instance)

@receiver(post_save, sender=Transaction)
def update_last_bought(sender, instance, **kwargs):
    """update products last_bought field on transaction"""
    instance.product.last_bought = instance.timestamp
    instance.product.save()

