from pytest import mark, fixture
from gelato_api.models import User
from gelato_api.serializers import OrderSerializer, UserSerializer

@fixture
def normal_user():
    class NormalUser():
        user = User.objects.create_user(email="super@user.com", password="12345", first_name="Super", last_name="User")
    return NormalUser()
@fixture
def superuser():
    class SuperUser():
        user = User.objects.create_superuser(email="super@user.com", password="12345", first_name="Super", last_name="User")
    return SuperUser()

@fixture
def models():
    class Models:
        user = User.objects.create_superuser(email="user@user.com", password="12345", first_name="User", last_name="User")
    return Models()

@mark.django_db
def test_create_from_UserSerializer_with_normal_user(normal_user):
    normal_user.data = {"password": "12345"}
    data = {
        "email": "test@test.com",
        "password": normal_user.data["password"],
        "is_staff": True,
        "is_superuser": True,
        "is_active": False
    }
    serializer = UserSerializer(context = {"request": normal_user}, data = data)
    serializer.is_valid()
    serializer.create(serializer.validated_data)
    assert data["password"] != serializer.validated_data["password"]
    assert data["is_staff"] != serializer.validated_data["is_staff"]
    assert data["is_superuser"] != serializer.validated_data["is_superuser"]
    assert data["is_active"] != serializer.validated_data["is_active"]

@mark.django_db
def test_create_from_UserSerializer_with_superuser(superuser):
    superuser.data = {"password": "12345"}
    data = {
        "email": "test@test.com",
        "password": superuser.data["password"],
        "is_staff": True,
        "is_superuser": True,
        "is_active": False
    }
    serializer = UserSerializer(context = {"request": superuser}, data = data)
    serializer.is_valid()
    serializer.create(serializer.validated_data)
    assert data["password"] != serializer.validated_data["password"]
    assert data["is_staff"] == serializer.validated_data["is_staff"]
    assert data["is_superuser"] == serializer.validated_data["is_superuser"]
    assert data["is_active"] == serializer.validated_data["is_active"]

@mark.django_db
def test_update_from_UserSerializer_with_normal_user(normal_user, models):
    normal_user.data = {"password": "12345"}
    data = {
        "email": "test@test.com",
        "password": normal_user.data["password"],
        "is_staff": True,
        "is_superuser": True,
        "is_active": False
    }
    serializer = UserSerializer(context = {"request": normal_user}, data = data)
    serializer.is_valid()
    serializer.update(models.user, serializer.validated_data)
    assert data["password"] != serializer.validated_data["password"]
    assert data["is_staff"] != serializer.validated_data["is_staff"]
    assert data["is_superuser"] != serializer.validated_data["is_superuser"]

@mark.django_db
def test_update_from_UserSerializer_with_superuser(superuser, models):
    superuser.data = {"password": "12345"}
    data = {
        "email": "test@test.com",
        "password": superuser.data["password"],
        "is_staff": True,
        "is_superuser": True,
        "is_active": False
    }
    serializer = UserSerializer(context = {"request": superuser}, data = data)
    serializer.is_valid()
    serializer.update(models.user, serializer.validated_data)
    assert data["password"] != serializer.validated_data["password"]
    assert data["is_staff"] == serializer.validated_data["is_staff"]
    assert data["is_superuser"] == serializer.validated_data["is_superuser"]

@mark.django_db
def test_create_from_OrderSerializer(superuser):
    data = {
        "comment": "comment_test",
        "delivery": True,
        "location": "location_test",
        "status": "...",
    }
    serializer = OrderSerializer(context = {"request": superuser}, data = data)
    serializer.is_valid()
    serializer.create(serializer.validated_data)
    assert serializer.validated_data["status"] == "Pedido solicitado"
    assert serializer.validated_data["user"] == superuser.user