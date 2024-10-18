from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action

from .permissions import *
from .models import Product, Category, Complement, Order, User
from .serializers import ProductSerializer, CategorySerializer, ComplementSerializer, OrderSerializer, UserSerializer

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all().order_by("id")
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'complements':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=["get"])
    def complements(self, request, pk=None):
        product = self.get_object()
        serializer = ComplementSerializer(Complement.objects.filter(categories__id=product.category.id), many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by("id")
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class ComplementViewSet(viewsets.ModelViewSet):
    serializer_class = ComplementSerializer
    queryset = Complement.objects.all().order_by("id")
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by("id")
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        elif self.action == 'destroy':
            permission_classes = [IsSuperuser]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by("id")
    permission_classes = [IsSuperuser]
    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [UserIsOwnerOrIsSuperuser]
        else:
            permission_classes = [IsSuperuser]
        return [permission() for permission in permission_classes]
        