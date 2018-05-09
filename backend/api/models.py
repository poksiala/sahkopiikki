from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class UserProfile(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def balance(self):
    return "{:.2f}€".format(-sum(map(lambda t: t.price, self.transactions.filter(done=False))) / 100)

  def __str__(self):
    if len(self.user.first_name) > 0:
      return "{} {}".format(self.user.first_name, self.user.last_name)
    else:
      return self.user.username

class Product(models.Model):
  name = models.CharField(max_length=200)
  price = models.IntegerField()
  price.help_text = 'In cents'
  image = models.ImageField(upload_to='uploaded_images/')

  def price_in_euros(self):
    return "{:.2f}€".format(self.price / 100)

  def __str__(self):
    return self.name

class Transaction(models.Model):
  user = models.ForeignKey('UserProfile', related_name='transactions', on_delete=models.SET_NULL, null=True)
  product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
  timestamp = models.DateTimeField(auto_now=True)
  price = models.IntegerField()
  price.help_text = 'In cents'
  done = models.BooleanField(default=False)

  def name(self):
    return self.__str__()

  def price_in_euros(self):
    return "{:.2f}€".format(self.price / 100)

  def __str__(self):
    return "{:.2f}€ to {}".format(self.price / 100, self.user)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)