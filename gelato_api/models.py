from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from os import urandom

def upload(instance, filename):
    return f"{instance.created_at.strftime('%d%m%y%H%M%S')}{urandom(5).hex()}-{filename.replace('-', '')}"

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, first_name, last_name, **extra_fields):
        if not email:
            raise ValueError("The given username must be set")
        if not password:
            raise ValueError("The given password must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, first_name, last_name, **extra_fields)

    def create_superuser(self, email, password, first_name, last_name, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(email, password, first_name, last_name, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)

    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']

    @property
    def last_login_date(self):
        if self.last_login:
            return self.last_login.strftime("%d/%m/%Y %H:%M:%S")
        return self.last_login
    @property
    def joined(self):
        return self.date_joined.strftime("%d/%m/%Y %H:%M:%S")

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.id} | {self.first_name} | {self.email}"

class Item(models.Model):
    in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def created(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")
    @property
    def updated(self):
        return self.updated_at.strftime("%d/%m/%Y %H:%M:%S")

    class Meta:
        abstract = True

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def created(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return f"Categoria Nº {self.id}: {self.name}"

class Complement(Item):
    name = models.CharField(max_length=255, unique=True)
    increase_value = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to=upload, null=True)
    categories = models.ManyToManyField(Category, related_name="complements")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="complements_created")
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="complements_updated")

    class Meta:
        verbose_name = "Complemento"
        verbose_name_plural = "Complementos"

    def __str__(self):
        return f"Complemento Nº {self.id}: {self.name}"

class Product(Item):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to=upload, null=True)
    max_complements = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products_created")
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="products_updated")

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"

    def __str__(self):
        return f"Produto Nº {self.id}: {self.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    delivery = models.BooleanField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def created(self):
        return self.created_at.strftime("%d/%m/%Y %H:%M:%S")
    
    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return f"Pedido Nº {self.id}: {self.status}"