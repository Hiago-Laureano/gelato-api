from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import Product, Category, Complement, Order, User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "description",
            "image",
            "max_complements",
            "in_stock",
            "category",
            "created",
            "updated",
        ]
        extra_kwargs = {
            "image": {"max_length": 30},
            "in_stock": {"default": True}
        }
    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
    def update(self, instance,validated_data):
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "created"
        ]

class ComplementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complement
        fields = [
            "id",
            "name",
            "increase_value",
            "image",
            "categories",
            "created",
            "updated"
        ]
        extra_kwargs = {
            "in_stock": {"default": True},
            "increase_value": {"default": 0.00}
        }

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
    def update(self, instance,validated_data):
        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "comment",
            "delivery",
            "location",
            "status",
            "active",
            "created"
        ]
        extra_kwargs = {
            "active": {"default": True},
            "status": {"default": "Pedido solicitado"}
        }
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        validated_data["status"] = "Pedido solicitado"
        return super().create(validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "is_superuser",
            "last_login_date",
            "joined"
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }
    def create(self, validated_data):
        validated_data["password"] = make_password(self.context["request"].data["password"])
        if not (self.context["request"].user.is_superuser):
            validated_data["is_staff"] = False
            validated_data["is_superuser"] = False
            validated_data["is_active"] = True
        return super().create(validated_data)
    def update(self, instance, validated_data):
        if "password" in self.context["request"].data:
            validated_data["password"] = make_password(self.context["request"].data["password"])
        if not (self.context["request"].user.is_superuser):
            validated_data["is_staff"] = False
            validated_data["is_superuser"] = False
        return super().update(instance, validated_data)