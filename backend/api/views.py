"""
Sähköpiikki views.
"""
from django.contrib.auth.models import User
from rest_framework import viewsets

from api.models import UserProfile, Transaction, Product
from api.serializers import (
    UserSerializer, UserProfileSerializer,
    ProductSerializer, TransactionSerializer
)

class UserViewset(viewsets.ReadOnlyModelViewSet):
  """User viewset."""
  queryset = User.objects.all()
  serializer_class = UserSerializer

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
  """User Profile viewset."""
  queryset = UserProfile.objects.filter(visible=True)
  serializer_class = UserProfileSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
  """Product viewset."""
  queryset = Product.objects.filter(visible=True)
  serializer_class = ProductSerializer

class TransactionViewSet(viewsets.ModelViewSet):
  """Transaction viewset."""
  queryset = Transaction.objects.all()
  serializer_class = TransactionSerializer
