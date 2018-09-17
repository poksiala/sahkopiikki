"""
Sähköpiikki views.
"""
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response

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
    queryset = UserProfile.objects.filter(visible=True).order_by('user__first_name')
    serializer_class = UserProfileSerializer

    def get_queryset(self):
        """ Get Queryset
        If requester is authenticated and is included in the
        queryset he/she will be returned as a first result

        Small increase in database load but should not matter in
        this context
        """
        user = self.request.user
        if not user.is_anonymous:
            requester = self.queryset.filter(user=user)
            rest = self.queryset.exclude(user=user)
            return list(requester) + list(rest)
        return self.queryset

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Product viewset."""
    queryset = Product.objects.filter(visible=True).order_by('-last_bought')
    serializer_class = ProductSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    """Transaction viewset."""
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

