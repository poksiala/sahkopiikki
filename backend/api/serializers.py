"""
Model serializers.
"""
from django.contrib.auth.models import User
from rest_framework import serializers
from api.models import UserProfile, Product, Transaction


class UserSerializer(serializers.HyperlinkedModelSerializer):
  """User model serializer."""
  class Meta:
    model = User
    fields = ('id', 'url', 'username', 'email', 'first_name', 'last_name')


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):
  """User Profile model serializer."""
  user = UserSerializer()

  class Meta:
    model = UserProfile
    fields = ('id', 'user', 'balance')
    depth = 1

class ProductSerializer(serializers.HyperlinkedModelSerializer):
  """Product model serializer."""
  class Meta:
    model = Product
    fields = ('id', 'name', 'price', 'image')

class TransactionSerializer(serializers.HyperlinkedModelSerializer):
  """Transaction model serializer."""
  user = UserProfileSerializer(read_only=True)
  product = ProductSerializer(read_only=True)
  user_id = serializers.PrimaryKeyRelatedField(source='user', queryset=UserProfile.objects.all())
  product_id = serializers.PrimaryKeyRelatedField(source='product', queryset=Product.objects.all())

  class Meta:
    model = Transaction
    fields = ('id', 'user', 'user_id', 'product', 'product_id', 'timestamp', 'price')
    depth = 1
